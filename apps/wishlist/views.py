from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Product

from .models import WishedProduct


@login_required
def page(request):
    items = WishedProduct.objects.filter(user=request.user).select_related("product")
    return render(request, "wishlist/page.html", {"items": items})


@login_required
@require_POST
def toggle(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    existing = WishedProduct.objects.filter(user=request.user, product=product).first()
    if existing:
        existing.delete()
        in_wishlist = False
    else:
        WishedProduct.objects.create(user=request.user, product=product)
        in_wishlist = True
    if request.headers.get("HX-Request"):
        return render(
            request,
            "wishlist/_heart.html",
            {"product": product, "in_wishlist": in_wishlist},
        )
    return redirect(request.META.get("HTTP_REFERER", "/"))
