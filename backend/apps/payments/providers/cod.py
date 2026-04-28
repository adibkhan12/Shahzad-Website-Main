from .base import PaymentProvider, PaymentStart, frontend_return_urls


class CODProvider(PaymentProvider):
    key = "cod"

    def start(self, order, request):
        return PaymentStart(redirect_url=frontend_return_urls(order)["success"])

    def verify(self, order, request):
        return False  # COD remains unpaid until delivered
