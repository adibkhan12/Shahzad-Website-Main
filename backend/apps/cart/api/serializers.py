from rest_framework import serializers

from apps.cart.models import Cart, CartItem
from apps.catalog.api.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "added_at", "line_total"]
        read_only_fields = ["id", "added_at", "line_total"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "subtotal", "count", "updated_at"]
