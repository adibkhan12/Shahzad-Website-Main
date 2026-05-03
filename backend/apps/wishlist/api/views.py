"""
Wishlist API — REST endpoints, all auth-required, all user-scoped.

Routes mounted at /api/v1/wishlist/:
  GET    /                      → list authenticated user's wishlist entries
  POST   /                      → add a product (body: {"product_id": <int>})
  DELETE /<product_id>/         → remove a product
  POST   /toggle/<product_id>/  → toggle in one call (idempotent convenience)
  GET    /check/<product_id>/   → {"in_wishlist": bool}

Safety:
  - Every query is filtered by request.user — no user can ever see/mutate another's list.
  - Unique-together (user, product) at the DB layer + get_or_create for race safety.
  - 404 for a missing product; the API never leaks existence of other users' rows.
"""

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Product
from apps.wishlist.models import WishedProduct

from .serializers import WishedProductSerializer


def _product_qs():
    """Prefetch helper — avoid N+1 on list serialization."""
    return Product.objects.select_related("brand", "category").prefetch_related("uploaded_images")


class WishlistView(APIView):
    """List (GET) and add (POST) for the current user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = (
            WishedProduct.objects.filter(user=request.user)
            .select_related("product", "product__brand", "product__category")
            .prefetch_related("product__uploaded_images")
        )
        return Response(
            WishedProductSerializer(items, many=True, context={"request": request}).data
        )

    def post(self, request):
        pid = request.data.get("product_id") or request.data.get("product")
        if not pid:
            return Response(
                {"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        product = get_object_or_404(_product_qs(), pk=pid, is_active=True)
        try:
            entry, created = WishedProduct.objects.get_or_create(
                user=request.user,
                product=product,
            )
        except IntegrityError:
            # Extremely unlikely given get_or_create, but belt-and-braces
            # against truly-concurrent INSERTs slipping past the SELECT.
            entry = WishedProduct.objects.get(user=request.user, product=product)
            created = False
        data = WishedProductSerializer(entry, context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class WishlistItemView(APIView):
    """Remove a product from the current user's wishlist."""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        deleted, _ = WishedProduct.objects.filter(
            user=request.user,
            product_id=product_id,
        ).delete()
        if not deleted:
            return Response({"detail": "Not in wishlist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistToggleView(APIView):
    """Idempotent single-call toggle — most frontends use this."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        existing = WishedProduct.objects.filter(user=request.user, product=product).first()
        if existing:
            existing.delete()
            return Response({"in_wishlist": False, "product_id": product.id})
        try:
            WishedProduct.objects.create(user=request.user, product=product)
        except IntegrityError:
            # Concurrent double-click — the other request won; treat as added.
            pass
        return Response({"in_wishlist": True, "product_id": product.id})


class WishlistCheckView(APIView):
    """Probe endpoint — useful for pages that don't want the full list."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        in_wishlist = WishedProduct.objects.filter(
            user=request.user,
            product_id=product_id,
        ).exists()
        return Response({"in_wishlist": in_wishlist, "product_id": int(product_id)})
