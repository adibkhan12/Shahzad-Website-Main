import requests
from django.conf import settings
from django.urls import reverse

from .base import PaymentProvider, PaymentStart


class TabbyProvider(PaymentProvider):
    key = "tabby"

    def start(self, order, request):
        base = settings.TABBY_API_URL
        secret = settings.TABBY_SECRET_KEY
        success_url = request.build_absolute_uri(
            reverse("payments:return_success", args=["tabby", order.reference])
        )
        cancel_url = request.build_absolute_uri(
            reverse("payments:return_cancel", args=["tabby", order.reference])
        )
        if not base or not secret:
            return PaymentStart(redirect_url=success_url, provider_ref="sandbox")

        payload = {
            "payment": {
                "amount": str(order.total),
                "currency": order.currency,
                "buyer": {"email": order.email, "name": order.name, "phone": order.phone},
                "shipping_address": {
                    "city": order.city,
                    "address": f"{order.address_line1} {order.address_line2}".strip(),
                    "zip": order.postal_code,
                },
                "order": {
                    "reference_id": str(order.reference),
                    "items": [
                        {
                            "title": i.title,
                            "quantity": i.quantity,
                            "unit_price": str(i.unit_price),
                            "reference_id": f"SKU-{i.product_id or i.id}",
                        }
                        for i in order.items.all()
                    ],
                },
            },
            "lang": "en",
            "merchant_code": "AE",
            "merchant_urls": {
                "success": success_url,
                "cancel": cancel_url,
                "failure": cancel_url,
            },
        }
        r = requests.post(
            f"{base.rstrip('/')}/api/v2/checkout",
            json=payload,
            headers={"Authorization": f"Bearer {secret}", "Content-Type": "application/json"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        web_url = (
            data.get("configuration", {})
            .get("available_products", {})
            .get("installments", [{}])[0]
            .get("web_url")
        )
        return PaymentStart(
            redirect_url=web_url or success_url,
            provider_ref=data.get("id", ""),
        )

    def verify(self, order, request):
        return True
