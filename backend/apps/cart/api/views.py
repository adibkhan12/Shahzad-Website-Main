from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.models import Cart, CartItem
from apps.cart.services import normalize_guest_session_key
from apps.catalog.models import Product

from .serializers import CartSerializer


def resolve_cart(request, create=True) -> Cart | None:
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    raw_session_key = (
        request.headers.get("X-Guest-Session") or request.data.get("session_key")
        if hasattr(request, "data")
        else request.headers.get("X-Guest-Session")
    )
    if not raw_session_key:
        raw_session_key = request.headers.get("X-Guest-Session")
    session_key = normalize_guest_session_key(raw_session_key)
    if not session_key:
        if not create:
            return None
        return None
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


class CartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = resolve_cart(request)
        if cart is None:
            return Response({"items": [], "subtotal": "0.00", "count": 0})
        return Response(CartSerializer(cart).data)


class CartAddView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        product_id = request.data.get("product_id")
        try:
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response({"detail": "Quantity must be a whole number."}, status=400)
        quantity = min(max(1, quantity), 99)
        product = Product.objects.filter(pk=product_id).first()
        if not product:
            return Response({"detail": "Product not found."}, status=404)
        cart = resolve_cart(request)
        if cart is None:
            return Response({"detail": "Missing X-Guest-Session for guest cart."}, status=400)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )
        if not created:
            item.quantity = item.quantity + quantity
            item.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartItemView(APIView):
    permission_classes = [permissions.AllowAny]

    def _item(self, request, item_id):
        cart = resolve_cart(request, create=False)
        if cart is None:
            return None, None
        return cart, CartItem.objects.filter(pk=item_id, cart=cart).first()

    def patch(self, request, item_id):
        cart, item = self._item(request, item_id)
        if item is None:
            return Response({"detail": "Not found."}, status=404)
        try:
            qty = int(request.data.get("quantity", item.quantity))
        except (TypeError, ValueError):
            return Response({"detail": "Quantity must be a whole number."}, status=400)
        if qty <= 0:
            item.delete()
        else:
            item.quantity = min(qty, 99)
            item.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        cart, item = self._item(request, item_id)
        if item is None:
            return Response({"detail": "Not found."}, status=404)
        item.delete()
        return Response(CartSerializer(cart).data)


class CartClearView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        cart = resolve_cart(request, create=False)
        if cart is None:
            return Response({"items": [], "subtotal": "0.00", "count": 0})
        cart.items.all().delete()
        return Response(CartSerializer(cart).data)


class CartMergeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from apps.cart.services import merge_guest_cart_into_user

        session_key = request.data.get("session_key") or request.headers.get("X-Guest-Session")
        if session_key:
            merge_guest_cart_into_user(request.user, session_key)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)
