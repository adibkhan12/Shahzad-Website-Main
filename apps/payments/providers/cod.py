from django.urls import reverse

from .base import PaymentProvider, PaymentStart


class CODProvider(PaymentProvider):
    key = "cod"

    def start(self, order, request):
        # COD: nothing to verify externally — go straight to thank-you, mark pending.
        return PaymentStart(redirect_url=reverse("payments:thank_you", args=[order.reference]))

    def verify(self, order, request):
        return False  # COD stays unpaid until delivered
