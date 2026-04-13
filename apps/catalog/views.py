from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .forms import QuestionForm, ReviewForm
from .models import AdBanner, Category, Product, QA, Review


def home(request):
    banners = list(AdBanner.objects.all()[:3])
    featured = list(Product.objects.filter(is_featured=True)[:3])
    new_products = list(Product.objects.order_by("-created_at")[:8])
    categories = list(Category.objects.filter(parent__isnull=True)[:6])
    return render(
        request,
        "catalog/home.html",
        {
            "banners": banners,
            "featured": featured,
            "new_products": new_products,
            "categories": categories,
        },
    )


def product_list(request):
    qs = Product.objects.all()
    q = request.GET.get("q", "").strip()
    brand = request.GET.get("brand", "").strip()
    sort = request.GET.get("sort", "").strip()
    category_slug = request.GET.get("category", "").strip()

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if brand:
        qs = qs.filter(brand__iexact=brand)
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if sort == "price_asc":
        qs = qs.order_by("price")
    elif sort == "price_desc":
        qs = qs.order_by("-price")
    elif sort == "name_asc":
        qs = qs.order_by("title")

    categories = Category.objects.filter(parent__isnull=True)
    brands = Product.objects.exclude(brand="").values_list("brand", flat=True).distinct()
    return render(
        request,
        "catalog/product_list.html",
        {
            "products": qs,
            "categories": categories,
            "brands": brands,
            "q": q,
            "sort": sort,
            "current_brand": brand,
            "current_category": category_slug,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    stats = product.reviews.aggregate(avg=Avg("rating"), count=Count("id"))
    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "related": related,
            "reviews": product.reviews.all()[:20],
            "qas": product.qas.all()[:20],
            "review_form": ReviewForm(initial={"rating": 5}),
            "question_form": QuestionForm(),
            "rating_avg": stats["avg"] or 0,
            "rating_count": stats["count"] or 0,
        },
    )


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(
        request,
        "catalog/category_detail.html",
        {"category": category, "products": products},
    )


@require_POST
def review_create(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        if request.user.is_authenticated and not review.user:
            review.user = request.user.get_full_name() or request.user.email
        review.save()
    if request.headers.get("HX-Request"):
        stats = product.reviews.aggregate(avg=Avg("rating"), count=Count("id"))
        return render(
            request,
            "catalog/_reviews_block.html",
            {
                "product": product,
                "reviews": product.reviews.all()[:20],
                "review_form": ReviewForm(initial={"rating": 5}),
                "rating_avg": stats["avg"] or 0,
                "rating_count": stats["count"] or 0,
            },
        )
    return product_detail(request, product.slug)


@require_POST
def question_create(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    form = QuestionForm(request.POST)
    if form.is_valid():
        qa = form.save(commit=False)
        qa.product = product
        if request.user.is_authenticated and not qa.user:
            qa.user = request.user.get_full_name() or request.user.email
        qa.save()
    if request.headers.get("HX-Request"):
        return render(
            request,
            "catalog/_qa_block.html",
            {"product": product, "qas": product.qas.all()[:20], "question_form": QuestionForm()},
        )
    return product_detail(request, product.slug)
