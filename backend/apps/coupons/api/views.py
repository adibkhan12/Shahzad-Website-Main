from decimal import Decimal

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api.views import resolve_cart
from apps.coupons.models import Coupon


class ValidateCouponView(APIView):
    """
    POST /api/v1/coupons/validate/
    Body: { "code": "WELCOME10", "region": "UAE" }

    Validates against the current cart server-side. Returns the resolved
    discount so the frontend can show it in the order summary. Re-validated
    at checkout time — this endpoint is advisory.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        code = (request.data.get("code") or "").strip().upper()
        region = (request.data.get("region") or "UAE").upper()
        if not code:
            return Response({"valid": False, "message": "Enter a coupon code."}, status=400)

        coupon = Coupon.objects.filter(code=code).first()
        if coupon is None:
            return Response({"valid": False, "message": "Coupon code not recognised."}, status=404)

        cart = resolve_cart(request, create=False)
        if cart is None or not cart.items.exists():
            return Response(
                {"valid": False, "message": "Your cart is empty."}, status=400
            )

        items = list(cart.items.select_related("product"))
        subtotal = sum((i.line_total for i in items), Decimal("0"))

        ok, message = coupon.validate_for(
            subtotal=subtotal,
            region=region,
            user=request.user if request.user.is_authenticated else None,
            cart_items=items,
        )
        if not ok:
            return Response({"valid": False, "message": message}, status=200)

        discount = coupon.compute_discount(subtotal)
        return Response(
            {
                "valid": True,
                "code": coupon.code,
                "discount_amount": str(discount),
                "discount_type": coupon.discount_type,
                "discount_value": str(coupon.discount_value),
                "message": f"Coupon applied — you save AED {discount:.2f}.",
            }
        )
