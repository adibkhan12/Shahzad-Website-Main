from rest_framework import serializers

from apps.repairs.models import RepairBooking, RepairService


class RepairServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairService
        fields = [
            "id",
            "name",
            "slug",
            "device",
            "short_desc",
            "description",
            "base_price",
            "est_minutes",
            "icon",
            "is_featured",
            "order",
        ]


class RepairBookingSerializer(serializers.ModelSerializer):
    short_ref = serializers.CharField(read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)
    service_slug = serializers.CharField(source="service.slug", read_only=True)

    class Meta:
        model = RepairBooking
        fields = [
            "id",
            "reference",
            "short_ref",
            "service",
            "service_name",
            "service_slug",
            "name",
            "email",
            "phone",
            "device_brand",
            "device_model",
            "issue",
            "preferred_drop_off",
            "quoted_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "reference",
            "short_ref",
            "quoted_price",
            "status",
            "created_at",
            "updated_at",
            "service_name",
            "service_slug",
        ]


class RepairStatusSerializer(serializers.Serializer):
    reference = serializers.UUIDField()
    phone = serializers.CharField()
