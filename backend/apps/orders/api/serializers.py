from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "title", "unit_price", "quantity", "image", "line_total"]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    short_ref = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "reference", "short_ref", "user",
            "name", "email", "phone", "address_line1", "address_line2",
            "city", "postal_code", "country",
            "currency", "subtotal", "total",
            "payment_method", "provider", "provider_ref", "paid", "status",
            "referral_source", "referral_other",
            "items", "created_at", "updated_at",
        ]
        read_only_fields = fields


class OrderTrackSerializer(serializers.Serializer):
    reference = serializers.UUIDField()
    email = serializers.EmailField()
