import requests
from django.conf import settings
from django.urls import reverse

from .base import PaymentProvider, PaymentStart


class TamaraProvider(PaymentProvider):
    key = "tamara"

    def start(self, order, request):
        base = settings.TAMARA_BASE_URL
        api_key = settings.TAMARA_API_KEY
        success_url = request.build_absolute_uri(
            reverse("payments:return_success", args=["tamara", order.reference])
        )
        cancel_url = request.build_absolute_uri(
            reverse("payments:return_cancel", args=["tamara", order.reference])
        )
        # When keys not configured yet, fall through to success URL (sandbox-less mode).
        if not base or not api_key:
            return PaymentStart(redirect_url=success_url, provider_ref="sandbox")

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
                "success": success_url,
                "failure": cancel_url,
                "cancel": cancel_url,
                "notification": request.build_absolute_uri(reverse("payments:webhook", args=["tamara"])),
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
            redirect_url=data.get("checkout_url") or data.get("redirect_url") or success_url,
            provider_ref=data.get("order_id", ""),
        )

    def verify(self, order, request):
        # In production: call Tamara's order-status endpoint and confirm "approved" / "authorised".
        # For now, trust the success callback (same as the old Next.js app).
        return True
