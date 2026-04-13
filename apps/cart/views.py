from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.catalog.models import Product

from .models import CartItem
from .services import get_or_create_cart


def cart_page(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/cart.html", {"cart": cart})


def _render_cart_partial(request, cart):
    return render(request, "cart/_cart_body.html", {"cart": cart})


def _render_badge(request, cart):
    return render(request, "cart/_badge.html", {"cart": cart})


@require_POST
def add(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    qty = max(1, int(request.POST.get("quantity", 1)))
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": qty}
    )
    if not created:
        item.quantity = item.quantity + qty
        item.save(update_fields=["quantity"])

    if request.headers.get("HX-Request"):
        response = _render_badge(request, cart)
        response["HX-Trigger"] = "cart:updated"
        return response
    return redirect("cart:page")


@require_POST
def update(request, item_id: int):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = int(request.POST.get("quantity", 1))
    if qty <= 0:
        item.delete()
    else:
        item.quantity = qty
        item.save(update_fields=["quantity"])
    if request.headers.get("HX-Request"):
        return _render_cart_partial(request, cart)
    return redirect("cart:page")


@require_POST
def remove(request, item_id: int):
    cart = get_or_create_cart(request)
    CartItem.objects.filter(pk=item_id, cart=cart).delete()
    if request.headers.get("HX-Request"):
        return _render_cart_partial(request, cart)
    return redirect("cart:page")


@require_POST
def clear(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    if request.headers.get("HX-Request"):
        return _render_cart_partial(request, cart)
    return redirect("cart:page")


def badge(request):
    cart = get_or_create_cart(request)
    return _render_badge(request, cart)
