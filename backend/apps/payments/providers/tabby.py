import logging

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError as DRFValidationError

from .base import PaymentProvider, PaymentStart, frontend_return_urls

# Tabby payment statuses that mean fulfillment is safe.
# Source: https://docs.tabby.ai/pay-in-4-custom-integration/payment-statuses.md
PAID_STATUSES = {"AUTHORIZED", "CLOSED"}

logger = logging.getLogger(__name__)


def _config_for(region: str) -> tuple[str, str, str]:
    """Return (api_url, secret_key, merchant_code) for the given region."""
    if region == "KSA":
        return (
            settings.TABBY_API_URL_KSA or "https://api.tabby.sa",
            settings.TABBY_SECRET_KEY_KSA or settings.TABBY_SECRET_KEY,
            settings.TABBY_MERCHANT_CODE_KSA or "SA",
        )
    return (
        settings.TABBY_API_URL_UAE or settings.TABBY_API_URL or "https://api.tabby.ai",
        settings.TABBY_SECRET_KEY_UAE or settings.TABBY_SECRET_KEY,
        settings.TABBY_MERCHANT_CODE_UAE or "AE",
    )


class TabbyProvider(PaymentProvider):
    key = "tabby"

    def start(self, order, request):
        base, secret, merchant_code = _config_for(order.region)
        urls = frontend_return_urls(order)
        if not base or not secret:
            return PaymentStart(redirect_url=urls["success"], provider_ref="sandbox")

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
            "merchant_code": merchant_code,
            "merchant_urls": {
                "success": urls["success"],
                "cancel": urls["cancel"],
                "failure": urls["cancel"],
            },
        }
        try:
            r = requests.post(
                f"{base.rstrip('/')}/api/v2/checkout",
                json=payload,
                headers={"Authorization": f"Bearer {secret}", "Content-Type": "application/json"},
                timeout=20,
            )
            r.raise_for_status()
        except requests.HTTPError as exc:
            body = (r.text or "")[:1000] if r is not None else "(no body)"
            logger.error(
                "Tabby API rejected checkout for order %s: %s — %s",
                order.reference,
                r.status_code,
                body,
            )
            detail = (
                f"Tabby is currently unavailable ({r.status_code}). "
                "Please choose a different payment method or try again shortly."
            )
            if settings.DEBUG:
                detail = f"Tabby {r.status_code}: {body}"
            raise DRFValidationError({"detail": detail}) from exc
        except requests.RequestException as exc:
            logger.exception("Tabby API call failed for order %s", order.reference)
            raise DRFValidationError(
                {"detail": "Could not reach Tabby — please try a different payment method."}
            ) from exc

        data = r.json()
        web_url = (
            data.get("configuration", {})
            .get("available_products", {})
            .get("installments", [{}])[0]
            .get("web_url")
        )
        return PaymentStart(
            redirect_url=web_url or urls["success"],
            provider_ref=data.get("id", ""),
        )

    def verify(self, order, request):
        """
        Confirm the order is genuinely paid by querying Tabby's payment endpoint.
        Returns True only if upstream `status` is in `PAID_STATUSES`.

        Source: https://docs.tabby.ai/api-reference/payments/retrieve-a-payment.md
        """
        if not order.provider_ref:
            return False
        base, secret, _ = _config_for(order.region)
        if not base or not secret:
            return False
        try:
            r = requests.get(
                f"{base.rstrip('/')}/api/v2/payments/{order.provider_ref}",
                headers={"Authorization": f"Bearer {secret}"},
                timeout=15,
            )
            r.raise_for_status()
        except requests.RequestException:
            return False
        return r.json().get("status") in PAID_STATUSES
