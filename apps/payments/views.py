from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.cart.services import get_or_create_cart
from apps.catalog.models import Product
from apps.orders.emails import send_order_confirmation
from apps.orders.models import Order, OrderItem

from .forms import CheckoutForm
from .providers import get_provider


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect("cart:page")

    initial = {}
    if request.user.is_authenticated:
        initial["email"] = request.user.email
        initial["name"] = (request.user.get_full_name() or "").strip() or request.user.email.split("@")[0]
        addr = request.user.addresses.filter(is_default=True).first() or request.user.addresses.first()
        if addr:
            initial.update(
                name=addr.name or initial.get("name"),
                phone=addr.phone,
                address_line1=addr.address_line1,
                address_line2=addr.address_line2,
                city=addr.city,
                postal_code=addr.postal_code,
                country=addr.country,
            )

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            return _place_order(request, cart, form.cleaned_data)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, "payments/checkout.html", {"form": form, "cart": cart})


@transaction.atomic
def _place_order(request, cart, data):
    subtotal = sum((i.line_total for i in cart.items.select_related("product")), Decimal("0"))

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        address_line1=data["address_line1"],
        address_line2=data["address_line2"],
        city=data["city"],
        postal_code=data["postal_code"],
        country=data["country"],
        currency=settings.CURRENCY,
        subtotal=subtotal,
        total=subtotal,
        payment_method=data["payment_method"],
        provider=data["payment_method"],
        referral_source=data.get("referral_source", ""),
        referral_other=data.get("referral_other", ""),
    )

    for ci in cart.items.select_related("product"):
        p = ci.product
        OrderItem.objects.create(
            order=order,
            product=p,
            title=p.title,
            unit_price=p.price,
            quantity=ci.quantity,
            image=p.primary_image,
        )

    # Stripe-shape line_items snapshot (kept for provider compat parity with old app)
    order.line_items = [
        {
            "price_data": {
                "product_data": {"name": i.title},
                "unit_amount": int(i.unit_price * 100),
                "currency": order.currency.lower(),
            },
            "quantity": i.quantity,
        }
        for i in order.items.all()
    ]
    order.save(update_fields=["line_items"])

    # Reserve stock atomically for COD (external providers decrement on capture).
    if data["payment_method"] == Order.PaymentMethod.COD:
        _decrement_stock(order)

    provider = get_provider(data["payment_method"])
    result = provider.start(order, request)
    if result.provider_ref:
        order.provider_ref = result.provider_ref
        order.save(update_fields=["provider_ref"])

    # Clear the cart now that the order has been created.
    cart.items.all().delete()

    send_order_confirmation(order)

    return redirect(result.redirect_url)


def _decrement_stock(order):
    for item in order.items.select_related("product"):
        if item.product:
            Product.objects.filter(pk=item.product_id, stock__gte=item.quantity).update(
                stock=models_F("stock") - item.quantity
            )


def _apply_payment(order):
    order.paid = True
    order.status = Order.Status.PAID
    order.save(update_fields=["paid", "status", "updated_at"])
    if order.payment_method != Order.PaymentMethod.COD:
        _decrement_stock(order)


def return_success(request, provider, reference):
    order = get_object_or_404(Order, reference=reference)
    prov = get_provider(provider)
    if prov.verify(order, request):
        _apply_payment(order)
    return redirect("payments:thank_you", reference=order.reference)


def return_cancel(request, provider, reference):
    order = get_object_or_404(Order, reference=reference)
    order.status = Order.Status.CANCELLED
    order.save(update_fields=["status", "updated_at"])
    messages.error(request, "Payment was cancelled. You can try again or choose another method.")
    return redirect("catalog:home")


@csrf_exempt
def webhook(request, provider):
    # Stub endpoint — production would verify signature and update the order.
    return HttpResponse(status=200)


def thank_you(request, reference):
    order = get_object_or_404(Order, reference=reference)
    return render(request, "payments/thank_you.html", {"order": order})


# Small shim to avoid importing django.db.models.F at module top (keeps the import block clean).
from django.db.models import F as models_F  # noqa: E402
