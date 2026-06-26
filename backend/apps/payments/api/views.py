from decimal import Decimal

import jwt
from django.conf import settings
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api.views import resolve_cart
from apps.catalog.models import Product
from apps.coupons.models import Coupon, CouponRedemption
from apps.orders.emails import send_order_confirmation
from apps.orders.models import Order, OrderItem
from apps.payments.providers import get_provider

from .serializers import CheckoutSerializer


def _decrement_stock(order):
    """Lock product rows and decrement stock. Must run inside transaction.atomic()."""
    for item in order.items.select_related("product"):
        if not item.product:
            continue
        product = Product.objects.select_for_update().filter(pk=item.product_id).first()
        if product is None:
            raise DRFValidationError({"detail": f"'{item.title}' is no longer available."})
        if product.stock < item.quantity:
            raise DRFValidationError(
                {"detail": f"Sorry, '{item.title}' only has {product.stock} left in stock."}
            )
        product.stock -= item.quantity
        product.save(update_fields=["stock"])


def _apply_payment(order):
    if order.paid:
        return
    order.paid = True
    order.status = Order.Status.PAID
    order.save(update_fields=["paid", "status", "updated_at"])
    if order.payment_method != Order.PaymentMethod.COD:
        _decrement_stock(order)


def _order_by_reference(reference):
    try:
        return Order.objects.select_for_update().filter(reference=reference).first()
    except (DjangoValidationError, TypeError, ValueError):
        return None


def _safe_order_response(order, request):
    from apps.orders.api.serializers import OrderSerializer

    if request.user.is_authenticated and order.user_id == request.user.id:
        return OrderSerializer(order).data
    return {
        "reference": str(order.reference),
        "short_ref": order.short_ref,
        "status": order.status,
        "paid": order.paid,
    }


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

        cart_items = list(cart.items.select_related("product"))
        subtotal = sum((i.line_total for i in cart_items), Decimal("0"))

        # Region-aware shipping fee.
        region = data.get("region", Order.Region.UAE)
        shipping_fee = Decimal(str(settings.SHIPPING[region]["fee"]))

        # Coupon — re-validate server-side, never trust the frontend.
        coupon_code = (data.get("coupon_code") or "").strip().upper()
        coupon = None
        discount_amount = Decimal("0")
        if coupon_code:
            coupon = Coupon.objects.filter(code=coupon_code).first()
            if coupon is None:
                raise DRFValidationError({"coupon_code": "Coupon code not recognised."})
            ok, message = coupon.validate_for(
                subtotal=subtotal,
                region=region,
                user=request.user if request.user.is_authenticated else None,
                cart_items=cart_items,
            )
            if not ok:
                raise DRFValidationError({"coupon_code": message})
            discount_amount = coupon.compute_discount(subtotal)

        total = subtotal + shipping_fee - discount_amount

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
            region=region,
            currency=settings.CURRENCY,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            bnpl_surcharge=Decimal("0"),
            coupon_code=coupon_code,
            discount_amount=discount_amount,
            total=total,
            payment_method=data["payment_method"],
            provider=data["payment_method"],
            referral_source=data.get("referral_source", ""),
            referral_other=data.get("referral_other", ""),
        )

        if coupon is not None:
            CouponRedemption.objects.create(
                coupon=coupon,
                user=request.user if request.user.is_authenticated else None,
                order=order,
                discount_amount=discount_amount,
            )
            Coupon.objects.filter(pk=coupon.pk).update(used_count=coupon.used_count + 1)

        for ci in cart.items.select_related("product"):
            p = ci.product
            OrderItem.objects.create(
                order=order,
                product=p,
                title=p.title,
                # effective_price honors any active sale_price; falls back to
                # regular price when there's no sale.
                unit_price=p.effective_price,
                quantity=ci.quantity,
                image=p.primary_image,
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

    @transaction.atomic
    def post(self, request):
        provider_key = request.data.get("provider")
        reference = request.data.get("reference")
        order = _order_by_reference(reference)
        if order is None:
            return Response({"detail": "Order not found."}, status=404)
        if provider_key != order.provider:
            return Response({"detail": "Payment provider does not match this order."}, status=400)
        try:
            provider = get_provider(provider_key)
        except ValueError:
            return Response({"detail": "Unknown payment provider."}, status=400)
        if provider.verify(order, request):
            _apply_payment(order)
        return Response(_safe_order_response(order, request))


class CancelView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Payment was cancelled."})
        reference = request.data.get("reference")
        try:
            order = Order.objects.filter(reference=reference, user=request.user).first()
        except (DjangoValidationError, TypeError, ValueError):
            order = None
        if order is None:
            return Response({"detail": "Order not found."}, status=404)
        if order.paid:
            return Response({"status": order.status})
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return Response({"status": order.status})


def _verify_tamara_jwt(request):
    """
    Tamara signs webhook auth as an HS256 JWT in the `Authorization: Bearer ...`
    header (or `?tamaraToken=...` query param). The signing secret is the
    Notification Token issued at webhook registration.

    Source: https://docs.tamara.co/docs/transaction-authorisation
    """
    secret = settings.TAMARA_NOTIFICATION_TOKEN
    if not secret:
        return None
    auth = request.headers.get("Authorization", "")
    token = auth[len("Bearer ") :] if auth.startswith("Bearer ") else None
    token = token or request.GET.get("tamaraToken")
    if not token:
        return None
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def _verify_tabby_secret(request):
    """
    Tabby's webhook auth header is merchant-configured. We document our
    convention as `X-Webhook-Auth` carrying a shared secret that matches
    `settings.TABBY_WEBHOOK_SECRET`. Configure the same value in the Tabby
    dashboard at webhook registration.

    Source: https://docs.tabby.ai/pay-in-4-custom-integration/webhooks.md
    """
    expected = settings.TABBY_WEBHOOK_SECRET
    if not expected:
        return False
    received = request.headers.get("X-Webhook-Auth", "")
    return constant_time_compare(received, expected)


def _process_payment_webhook(provider_key, provider_ref):
    """
    Common flow shared by both providers' webhook handlers:
    look up the order, defense-in-depth call to provider's GET endpoint to
    confirm status, apply payment if confirmed.

    Returns a (response_dict, status_code) tuple.
    """
    if not provider_ref:
        return {"detail": "Missing provider reference."}, 400

    with transaction.atomic():
        order = (
            Order.objects.select_for_update()
            .filter(provider_ref=provider_ref, provider=provider_key)
            .first()
        )
        if order is None:
            return {"detail": "Order not found."}, 404
        if get_provider(provider_key).verify(order, None):
            _apply_payment(order)
    return {"detail": "OK"}, 200


@csrf_exempt
@api_view(["POST"])
@authentication_classes([])  # webhook auth is provider-specific, not JWT — skip DRF auth
@permission_classes([permissions.AllowAny])
def webhook(request, provider):
    """
    Receives provider notifications. Verifies the request came from the
    provider, then trusts the provider's GET endpoint (not the webhook body)
    as the source of truth for the order's paid status — defense in depth.
    """
    if provider == "tamara":
        if _verify_tamara_jwt(request) is None:
            return Response({"detail": "Invalid Tamara token."}, status=401)
        provider_ref = request.data.get("order_id") or request.data.get("order_reference_id")
        body, code = _process_payment_webhook("tamara", provider_ref)
        return Response(body, status=code)

    if provider == "tabby":
        if not _verify_tabby_secret(request):
            return Response({"detail": "Invalid Tabby auth header."}, status=401)
        provider_ref = request.data.get("id")
        body, code = _process_payment_webhook("tabby", provider_ref)
        return Response(body, status=code)

    return Response({"detail": f"Unknown provider {provider!r}."}, status=404)
