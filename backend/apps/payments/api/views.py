from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api.views import resolve_cart
from apps.catalog.models import Product
from apps.orders.emails import send_order_confirmation
from apps.orders.models import Order, OrderItem
from apps.payments.providers import get_provider

from .serializers import CheckoutSerializer


def _decrement_stock(order):
    for item in order.items.select_related("product"):
        if item.product:
            Product.objects.filter(pk=item.product_id, stock__gte=item.quantity).update(
                stock=F("stock") - item.quantity
            )


def _apply_payment(order):
    order.paid = True
    order.status = Order.Status.PAID
    order.save(update_fields=["paid", "status", "updated_at"])
    if order.payment_method != Order.PaymentMethod.COD:
        _decrement_stock(order)


class CheckoutView(APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        ser = CheckoutSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        cart = resolve_cart(request, create=False)
        if cart is None or not cart.items.exists():
            return Response({"detail": "Cart is empty."}, status=400)

        subtotal = sum(
            (i.line_total for i in cart.items.select_related("product")),
            Decimal("0"),
        )

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            address_line1=data["address_line1"],
            address_line2=data.get("address_line2", ""),
            city=data["city"],
            postal_code=data.get("postal_code", ""),
            country=data.get("country", "UAE"),
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
                order=order, product=p, title=p.title,
                unit_price=p.price, quantity=ci.quantity, image=p.primary_image,
            )

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

        if data["payment_method"] == Order.PaymentMethod.COD:
            _decrement_stock(order)

        provider = get_provider(data["payment_method"])
        result = provider.start(order, request)
        if result.provider_ref:
            order.provider_ref = result.provider_ref
            order.save(update_fields=["provider_ref"])

        cart.items.all().delete()
        try:
            send_order_confirmation(order)
        except Exception:
            pass

        return Response(
            {"reference": str(order.reference), "redirect_url": result.redirect_url},
            status=status.HTTP_201_CREATED,
        )


class ConfirmView(APIView):
    """Frontend calls this after the provider redirects back with success."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        provider_key = request.data.get("provider")
        reference = request.data.get("reference")
        order = Order.objects.filter(reference=reference).first()
        if order is None:
            return Response({"detail": "Order not found."}, status=404)
        provider = get_provider(provider_key)
        if provider.verify(order, request):
            _apply_payment(order)
        from apps.orders.api.serializers import OrderSerializer
        return Response(OrderSerializer(order).data)


class CancelView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        reference = request.data.get("reference")
        order = Order.objects.filter(reference=reference).first()
        if order is None:
            return Response({"detail": "Order not found."}, status=404)
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return Response({"status": order.status})


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def webhook(request, provider):
    # Stub — production: verify signature, find order by provider_ref, apply payment.
    return Response(status=200)
