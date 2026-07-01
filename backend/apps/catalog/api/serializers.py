from django.db.models import Avg, Count
from rest_framework import serializers

from apps.catalog.models import QA, AdBanner, Brand, CatalogProperty, Category, ColorVariant, Product, Review, Setting


def _abs(request, url: str) -> str:
    if url and request and url.startswith("/"):
        return request.build_absolute_uri(url)
    return url or ""


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "parent",
            "image",
            "properties",
            "is_active",
            "order",
            "product_count",
        ]

    def get_image(self, obj) -> str:
        return _abs(self.context.get("request"), obj.image_url)


class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "category_name",
            "category_slug",
            "logo",
            "description",
            "is_active",
            "order",
        ]

    def get_logo(self, obj) -> str:
        return _abs(self.context.get("request"), obj.logo_url)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "text", "images", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"product": {"required": False}}


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ["id", "product", "user", "question", "answer", "created_at", "answered_at"]
        read_only_fields = ["id", "created_at", "answered_at", "answer"]
        extra_kwargs = {"product": {"required": False}}


class ColorVariantSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ColorVariant
        fields = ["id", "color_name", "price", "order", "images"]

    def get_images(self, obj) -> list[str]:
        request = self.context.get("request")
        return [
            _abs(request, img.image.url)
            for img in obj.images.order_by("order", "id")
            if img.image
        ]


class ProductListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    on_sale = serializers.BooleanField(read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    brand = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "sale_price",
            "effective_price",
            "on_sale",
            "primary_image",
            "images",
            "stock",
            "brand",
            "category",
            "category_slug",
            "category_name",
            "is_active",
            "is_featured",
        ]

    def get_primary_image(self, obj) -> str:
        return _abs(self.context.get("request"), obj.primary_image)

    def get_images(self, obj) -> list[str]:
        req = self.context.get("request")
        return [_abs(req, u) for u in obj.all_images]

    def get_brand(self, obj):
        if not obj.brand:
            return None
        return {"id": obj.brand.id, "name": obj.brand.name, "slug": obj.brand.slug}


class ProductDetailSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    on_sale = serializers.BooleanField(read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    rating_avg = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    color_variants_data = ColorVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "sale_price",
            "effective_price",
            "on_sale",
            "images",
            "primary_image",
            "stock",
            "has_color_variants",
            "is_price_same",
            "is_box_packed",
            "color_variants_data",
            "properties",
            "product_properties",
            "brand",
            "category",
            "is_active",
            "is_featured",
            "rating_avg",
            "rating_count",
            "created_at",
            "updated_at",
        ]

    def get_primary_image(self, obj) -> str:
        return _abs(self.context.get("request"), obj.primary_image)

    def get_images(self, obj) -> list[str]:
        req = self.context.get("request")
        return [_abs(req, u) for u in obj.all_images]

    def get_rating_avg(self, obj):
        return obj.reviews.aggregate(a=Avg("rating"))["a"] or 0

    def get_rating_count(self, obj):
        return obj.reviews.aggregate(c=Count("id"))["c"] or 0


class AdBannerSerializer(serializers.ModelSerializer):
    """Ad banner serializer with per-request localization.

    The frontend sends `Accept-Language: ar` (or `en`) on the site-config
    fetch; we return the Arabic copy (title_ar/desc_ar/button_ar) if set,
    falling back to English whenever the Arabic field is blank. Banners
    with partial translations degrade gracefully instead of showing nothing.
    """

    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    button = serializers.SerializerMethodField()

    class Meta:
        model = AdBanner
        fields = ["id", "title", "desc", "image", "button", "link", "bg", "order"]

    def get_image(self, obj) -> str:
        return _abs(self.context.get("request"), obj.image_url)

    def _is_arabic(self) -> bool:
        request = self.context.get("request")
        if not request:
            return False
        header = (request.headers.get("Accept-Language") or "").lower()
        # Match any Arabic variant (ar, ar-AE, ar-SA, etc.).
        return header.startswith("ar")

    def get_title(self, obj) -> str:
        if self._is_arabic() and obj.title_ar:
            return obj.title_ar
        return obj.title

    def get_desc(self, obj) -> str:
        if self._is_arabic() and obj.desc_ar:
            return obj.desc_ar
        return obj.desc

    def get_button(self, obj) -> str:
        if self._is_arabic() and obj.button_ar:
            return obj.button_ar
        return obj.button


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ["name", "value", "updated_at"]


class CatalogPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogProperty
        fields = ["id", "property_name", "property_values"]
