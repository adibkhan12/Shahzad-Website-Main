from rest_framework import serializers

from apps.catalog.api.serializers import ProductListSerializer
from apps.wishlist.models import WishedProduct


class WishedProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = WishedProduct
        fields = ["id", "product", "added_at"]
