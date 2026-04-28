from dataclasses import dataclass

from django.conf import settings


@dataclass
class PaymentStart:
    redirect_url: str | None
    provider_ref: str = ""


def frontend_return_urls(order):
    base = settings.FRONTEND_URL.rstrip("/")
    return {
        "success": f"{base}/checkout/return/{order.payment_method}/{order.reference}/success",
        "cancel": f"{base}/checkout/return/{order.payment_method}/{order.reference}/cancel",
    }


def backend_webhook_url(request, provider_key):
    return request.build_absolute_uri(f"/api/v1/payments/webhook/{provider_key}/")


class PaymentProvider:
    key: str = ""

    def start(self, order, request) -> PaymentStart:
        raise NotImplementedError

    def verify(self, order, request) -> bool:
        raise NotImplementedError
