from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.catalog.models import AdBanner, Brand, Category, HomePage, Product, QA, Review, Setting

from .serializers import (
    AdBannerSerializer,
    BrandSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    QASerializer,
    ReviewSerializer,
    SettingSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"

    @action(detail=False, methods=["get"])
    def roots(self, request):
        qs = Category.objects.filter(parent__isnull=True, is_active=True)
        return Response(CategorySerializer(qs, many=True, context={"request": request}).data)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True).select_related("category")
    serializer_class = BrandSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"category__slug": ["exact"], "category": ["exact"]}


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category", "brand")
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "brand__slug": ["exact"],
        "brand__name": ["exact", "iexact"],
        "brand": ["exact"],
        "category__slug": ["exact"],
        "is_featured": ["exact"],
    }
    search_fields = ["title", "description", "brand__name"]
    ordering_fields = ["price", "title", "created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        q = params.get("q", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(brand__name__icontains=q))
        sort = params.get("sort", "")
        if sort == "price_asc":
            qs = qs.order_by("price")
        elif sort == "price_desc":
            qs = qs.order_by("-price")
        elif sort == "name_asc":
            qs = qs.order_by("title")
        return qs

    @action(detail=False, methods=["get"])
    def featured(self, request):
        qs = Product.objects.filter(is_active=True, is_featured=True).select_related("brand", "category")[:12]
        products = list(qs)

        # Promote the admin-picked hero to index 0 so the homepage uses it.
        home = HomePage.objects.first()
        hero_id = home.hero_product_id if home else None
        if hero_id:
            idx = next((i for i, p in enumerate(products) if p.id == hero_id), None)
            if idx is not None:
                products.insert(0, products.pop(idx))
            else:
                # Hero isn't in the featured set — fetch and prepend it anyway.
                hero = (
                    Product.objects
                    .filter(id=hero_id, is_active=True)
                    .select_related("brand", "category")
                    .first()
                )
                if hero:
                    products.insert(0, hero)
                    products = products[:12]

        return Response(ProductListSerializer(products, many=True, context={"request": request}).data)

    @action(detail=False, methods=["get"])
    def bestsellers(self, request):
        """Top-selling products, ranked by total units sold on paid / shipped / delivered orders."""
        from django.db.models import Sum
        from apps.orders.models import OrderItem

        limit = int(request.query_params.get("limit") or 8)
        sold_ids = (
            OrderItem.objects
            .filter(
                order__status__in=["paid", "shipped", "delivered"],
                product__isnull=False,
                product__is_active=True,
            )
            .values("product_id")
            .annotate(units=Sum("quantity"))
            .order_by("-units")
            .values_list("product_id", flat=True)[:limit]
        )
        sold_ids = list(sold_ids)

        # Fall back to newest active products if we have too few sales yet
        if len(sold_ids) < limit:
            filler = list(
                Product.objects.filter(is_active=True)
                .exclude(id__in=sold_ids)
                .order_by("-created_at")
                .values_list("id", flat=True)[: limit - len(sold_ids)]
            )
            sold_ids += filler

        products = {
            p.id: p for p in
            Product.objects.filter(id__in=sold_ids).select_related("brand", "category")
        }
        ordered = [products[i] for i in sold_ids if i in products]
        return Response(ProductListSerializer(ordered, many=True, context={"request": request}).data)

    @action(detail=False, methods=["get"], url_path="by-brand/(?P<brand_name>[^/.]+)")
    def by_brand(self, request, brand_name=None):
        """Products across all categories for a given brand name (case-insensitive).
        Matches on brand name so 'apple' returns iPhones, MacBooks, iPads, etc.
        """
        limit = int(request.query_params.get("limit") or 8)
        qs = (
            Product.objects.filter(is_active=True, brand__name__iexact=brand_name)
            .select_related("brand", "category")[:limit]
        )
        return Response(ProductListSerializer(qs, many=True, context={"request": request}).data)

    @action(detail=False, methods=["get"])
    def brands(self, request):
        """
        Distinct brand names with the list of categories each brand appears in.
        The Brand model is one row per (name, category), so we group here to
        avoid "Apple, Apple, Apple…" in the storefront sidebar.
        Shape:
          [{"name": "Apple", "slug": "apple",
            "categories": [{"name": "Phones", "slug": "phones"}, ...]},
           ...]
        """
        qs = Brand.objects.filter(is_active=True).select_related("category").order_by("order", "name")
        category_slug = request.query_params.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        grouped: dict[str, dict] = {}
        for b in qs:
            key = b.name
            if key not in grouped:
                grouped[key] = {
                    "name": b.name,
                    "slug": b.slug,  # representative slug; frontend filters by name instead
                    "categories": [],
                }
            if b.category:
                cat_entry = {"name": b.category.name, "slug": b.category.slug}
                if cat_entry not in grouped[key]["categories"]:
                    grouped[key]["categories"].append(cat_entry)
        return Response(list(grouped.values()))

    @action(detail=True, methods=["get"])
    def reviews(self, request, slug=None):
        product = self.get_object()
        qs = product.reviews.all()[:50]
        return Response(ReviewSerializer(qs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def add_review(self, request, slug=None):
        product = self.get_object()
        ser = ReviewSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user_label = ser.validated_data.get("user") or ""
        if not user_label and request.user.is_authenticated:
            user_label = request.user.get_full_name() or request.user.email
        ser.save(product=product, user=user_label)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def qas(self, request, slug=None):
        product = self.get_object()
        qs = product.qas.all()[:50]
        return Response(QASerializer(qs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def add_question(self, request, slug=None):
        product = self.get_object()
        ser = QASerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user_label = ser.validated_data.get("user") or ""
        if not user_label and request.user.is_authenticated:
            user_label = request.user.get_full_name() or request.user.email
        ser.save(product=product, user=user_label)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def related(self, request):
        slug = request.query_params.get("slug")
        if not slug:
            return Response([])
        try:
            p = Product.objects.get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return Response([])
        qs = Product.objects.filter(is_active=True, category=p.category).exclude(pk=p.pk)[:4]
        return Response(ProductListSerializer(qs, many=True, context={"request": request}).data)


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdBanner.objects.filter(is_active=True)
    serializer_class = AdBannerSerializer


class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    lookup_field = "name"
