import logging

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError as DRFValidationError

from .base import PaymentProvider, PaymentStart, backend_webhook_url, frontend_return_urls

# Tamara order statuses that mean the customer has paid (or has a binding promise to pay).
# Source: https://docs.tamara.co/docs/online-order-status-flow
PAID_STATUSES = {"authorised", "fully_captured"}

# Maps our internal Region codes to Tamara's ISO country codes.
COUNTRY_CODE = {"UAE": "AE", "KSA": "SA"}

logger = logging.getLogger(__name__)


def _api_key_for(region: str) -> str:
    """UAE/KSA-specific Tamara key, falling back to the legacy single key."""
    if region == "KSA":
        return settings.TAMARA_API_KEY_KSA or settings.TAMARA_API_KEY
    return settings.TAMARA_API_KEY_UAE or settings.TAMARA_API_KEY


class TamaraProvider(PaymentProvider):
    key = "tamara"

    def start(self, order, request):
        base = settings.TAMARA_BASE_URL
        api_key = _api_key_for(order.region)
        urls = frontend_return_urls(order)
        if not base or not api_key:
            # Configured-out: skip the upstream call entirely. Used when a
            # merchant hasn't set up Tamara yet — order falls back to a
            # success-redirect placeholder.
            return PaymentStart(redirect_url=urls["success"], provider_ref="sandbox")

        country = COUNTRY_CODE.get(order.region, "AE")
        first = order.name.split(" ")[0] or order.name
        last = " ".join(order.name.split(" ")[1:]) or "-"

        # Address block — Tamara requires both `shipping_address` and
        # `billing_address`. We use the same data for both unless we ever
        # collect a separate billing address from the customer.
        # Source: https://docs.tamara.co/reference/createcheckoutsession
        address = {
            "first_name": first,
            "last_name": last,
            "line1": order.address_line1,
            "line2": order.address_line2 or "",
            "region": order.city,
            "city": order.city,
            "country_code": country,
            "phone_number": order.phone,
        }

        payload = {
            "order_reference_id": str(order.reference),
            "order_number": order.short_ref,
            "total_amount": {"amount": str(order.total), "currency": order.currency},
            "tax_amount": {"amount": "0", "currency": order.currency},
            "shipping_amount": {
                "amount": str(order.shipping_fee),
                "currency": order.currency,
            },
            "description": f"Order {order.short_ref} from Shahzad Mobile",
            "country_code": country,
            "payment_type": "PAY_BY_INSTALMENTS",
            "instalments": 4,
            "locale": "en_US",
            "platform": "Web",
            "is_mobile": False,
            "items": [
                {
                    "reference_id": str(i.id),
                    "type": "physical",
                    "name": i.title,
                    "sku": f"SKU-{i.product_id or i.id}",
                    "quantity": i.quantity,
                    "unit_price": {"amount": str(i.unit_price), "currency": order.currency},
                    "total_amount": {
                        "amount": str(i.unit_price * i.quantity),
                        "currency": order.currency,
                    },
                }
                for i in order.items.all()
            ],
            "consumer": {
                "first_name": first,
                "last_name": last,
                "phone_number": order.phone,
                "email": order.email,
            },
            "shipping_address": address,
            "billing_address": address,
            "merchant_url": {
                "success": urls["success"],
                "failure": urls["cancel"],
                "cancel": urls["cancel"],
                "notification": backend_webhook_url(request, "tamara"),
            },
        }
        try:
            r = requests.post(
                f"{base.rstrip('/')}/checkout",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                timeout=20,
            )
            r.raise_for_status()
        except requests.HTTPError as exc:
            # Tamara rejected our request. Log the upstream body so you can
            # see what's wrong, then surface a clean 400 to the customer.
            body = (r.text or "")[:1000] if r is not None else "(no body)"
            logger.error(
                "Tamara API rejected checkout for order %s: %s — %s",
                order.reference,
                r.status_code,
                body,
            )
            # In DEBUG, include Tamara's actual error in the response so you
            # can see it in the browser without digging in the runserver log.
            detail = (
                f"Tamara is currently unavailable ({r.status_code}). "
                "Please choose a different payment method or try again shortly."
            )
            if settings.DEBUG:
                detail = f"Tamara {r.status_code}: {body}"
            raise DRFValidationError({"detail": detail}) from exc
        except requests.RequestException as exc:
            logger.exception("Tamara API call failed for order %s", order.reference)
            raise DRFValidationError(
                {"detail": "Could not reach Tamara — please try a different payment method."}
            ) from exc

        data = r.json()
        return PaymentStart(
            redirect_url=data.get("checkout_url") or data.get("redirect_url") or urls["success"],
            provider_ref=data.get("order_id", ""),
        )

    def verify(self, order, request):
        """
        Confirm the order is genuinely paid by querying Tamara's order endpoint.
        Returns True only if the upstream `status` is in `PAID_STATUSES`.

        Source: https://docs.tamara.co/reference/getorderdetails
        """
        if not order.provider_ref:
            return False
        base = settings.TAMARA_BASE_URL
        api_key = _api_key_for(order.region)
        if not base or not api_key:
            return False
        try:
            r = requests.get(
                f"{base.rstrip('/')}/orders/{order.provider_ref}",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=15,
            )
            r.raise_for_status()
        except requests.RequestException:
            return False
        return r.json().get("status") in PAID_STATUSES
