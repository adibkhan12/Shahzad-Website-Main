import requests
from django.conf import settings

from .base import PaymentProvider, PaymentStart, backend_webhook_url, frontend_return_urls


class TamaraProvider(PaymentProvider):
    key = "tamara"

    def start(self, order, request):
        base = settings.TAMARA_BASE_URL
        api_key = settings.TAMARA_API_KEY
        urls = frontend_return_urls(order)
        if not base or not api_key:
            return PaymentStart(redirect_url=urls["success"], provider_ref="sandbox")

        payload = {
            "order_reference_id": str(order.reference),
            "total_amount": {"amount": str(order.total), "currency": order.currency},
            "items": [
                {
                    "reference_id": str(i.id),
                    "type": "physical",
                    "name": i.title,
                    "sku": f"SKU-{i.product_id or i.id}",
                    "quantity": i.quantity,
                    "unit_price": {"amount": str(i.unit_price), "currency": order.currency},
                    "total_amount": {"amount": str(i.line_total), "currency": order.currency},
                }
                for i in order.items.all()
            ],
            "consumer": {
                "first_name": order.name.split(" ")[0] or order.name,
                "last_name": " ".join(order.name.split(" ")[1:]) or "-",
                "phone_number": order.phone,
                "email": order.email,
            },
            "country_code": "AE",
            "payment_type": "PAY_BY_INSTALMENTS",
            "merchant_url": {
                "success": urls["success"],
                "failure": urls["cancel"],
                "cancel": urls["cancel"],
                "notification": backend_webhook_url(request, "tamara"),
            },
        }
        r = requests.post(
            f"{base.rstrip('/')}/checkout",
            json=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        return PaymentStart(
            redirect_url=data.get("checkout_url") or data.get("redirect_url") or urls["success"],
            provider_ref=data.get("order_id", ""),
        )

    def verify(self, order, request):
        return True
