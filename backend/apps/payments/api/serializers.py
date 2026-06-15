from django.conf import settings
from rest_framework import serializers

from apps.orders.models import Order


class CheckoutSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=40)
    address_line1 = serializers.CharField(max_length=255)
    address_line2 = serializers.CharField(required=False, allow_blank=True, max_length=255)
    city = serializers.CharField(max_length=120)
    postal_code = serializers.CharField(required=False, allow_blank=True, max_length=20)
    country = serializers.CharField(max_length=80, required=False, default="UAE")
    region = serializers.ChoiceField(
        choices=[c[0] for c in Order.Region.choices], default=Order.Region.UAE
    )
    payment_method = serializers.ChoiceField(choices=[c[0] for c in Order.PaymentMethod.choices])
    coupon_code = serializers.CharField(required=False, allow_blank=True, max_length=32)
    referral_source = serializers.CharField(required=False, allow_blank=True, max_length=64)
    referral_other = serializers.CharField(required=False, allow_blank=True, max_length=255)

    def validate(self, data):
        # KSA delivery is limited to specific cities. Reject anything else
        # before we create the order or hit a payment provider.
        if data.get("region") == Order.Region.KSA:
            allowed = {c.lower() for c in settings.KSA_ALLOWED_CITIES}
            if data["city"].strip().lower() not in allowed:
                raise serializers.ValidationError(
                    {
                        "city": (
                            f"For KSA we currently only deliver to: "
                            f"{', '.join(settings.KSA_ALLOWED_CITIES)}."
                        )
                    }
                )
        return data
