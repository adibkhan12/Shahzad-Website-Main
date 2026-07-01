import logging

import stripe
from django.conf import settings
from rest_framework.exceptions import ValidationError as DRFValidationError

from .base import PaymentProvider, PaymentStart, frontend_return_urls

logger = logging.getLogger(__name__)


class StripeProvider(PaymentProvider):
    key = "card"

    def start(self, order, request):
        secret = settings.STRIPE_SECRET_KEY
        urls = frontend_return_urls(order)
        if not secret:
            return PaymentStart(redirect_url=urls["success"], provider_ref="sandbox")

        stripe.api_key = secret
        try:
            session = stripe.checkout.Session.create(
                client_reference_id=str(order.reference),
                customer_email=order.email,
                line_items=[
                    {
                        "price_data": {
                            "currency": order.currency.lower(),
                            "product_data": {"name": f"Order {order.short_ref} — Shahzad Mobile"},
                            # Stripe amounts are in the smallest currency unit (fils for AED).
                            "unit_amount": int(order.total * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                # {CHECKOUT_SESSION_ID} is a Stripe template variable — do not change.
                success_url=urls["success"] + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=urls["cancel"],
                payment_method_types=["card"],
            )
        except stripe.StripeError as exc:
            logger.exception("Stripe session creation failed for order %s", order.reference)
            detail = "Card payment is currently unavailable. Please choose a different payment method."
            if settings.DEBUG:
                detail = f"Stripe error: {exc}"
            raise DRFValidationError({"detail": detail}) from exc

        return PaymentStart(redirect_url=session.url, provider_ref=session.id)

    def verify(self, order, request):
        """
        Retrieve the Checkout Session from Stripe and confirm payment_status == 'paid'.
        Called both from the frontend redirect (ConfirmView) and the webhook handler.
        """
        if not order.provider_ref or order.provider_ref == "sandbox":
            return False
        secret = settings.STRIPE_SECRET_KEY
        if not secret:
            return False
        stripe.api_key = secret
        try:
            session = stripe.checkout.Session.retrieve(order.provider_ref)
        except stripe.StripeError:
            logger.exception("Stripe session retrieval failed for order %s", order.reference)
            return False
        return session.payment_status == "paid"
