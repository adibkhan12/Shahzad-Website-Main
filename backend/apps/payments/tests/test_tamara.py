"""
Golden tests for the Tamara payment provider.

Covers `TamaraProvider.verify()` (which calls `GET /orders/{id}` upstream)
and the `/api/v1/payments/webhook/tamara/` view (JWT-auth + defense-in-depth
status check).

Mocked using `responses` so we test against the documented API contract
without needing real sandbox keys.
"""

from decimal import Decimal
from unittest.mock import MagicMock

import jwt
import pytest
import responses

from apps.orders.models import Order, OrderItem
from apps.payments.providers.tamara import TamaraProvider

TAMARA_BASE = "https://api-sandbox.tamara.co"
TAMARA_API_KEY = "test-tamara-api-key"
TAMARA_NOTIFICATION_TOKEN = "test-tamara-notification-secret"


@pytest.fixture
def tamara_settings(settings):
    settings.TAMARA_BASE_URL = TAMARA_BASE
    settings.TAMARA_API_KEY = TAMARA_API_KEY
    settings.TAMARA_NOTIFICATION_TOKEN = TAMARA_NOTIFICATION_TOKEN
    return settings


def _stub_order(ref="tamara-order-abc"):
    """Lightweight order stub for verify() — avoids DB."""
    return MagicMock(provider_ref=ref)


# --------------------------------------------------------------------------- #
# TamaraProvider.verify()
# --------------------------------------------------------------------------- #


@responses.activate
def test_verify_returns_true_for_authorised(tamara_settings):
    responses.add(
        responses.GET,
        f"{TAMARA_BASE}/orders/tamara-order-abc",
        json={"order_id": "tamara-order-abc", "status": "authorised"},
        status=200,
    )

    assert TamaraProvider().verify(_stub_order(), None) is True


@responses.activate
def test_verify_returns_true_for_fully_captured(tamara_settings):
    responses.add(
        responses.GET,
        f"{TAMARA_BASE}/orders/tamara-order-abc",
        json={"status": "fully_captured"},
        status=200,
    )

    assert TamaraProvider().verify(_stub_order(), None) is True


@responses.activate
def test_verify_returns_false_for_declined(tamara_settings):
    responses.add(
        responses.GET,
        f"{TAMARA_BASE}/orders/tamara-order-abc",
        json={"status": "declined"},
        status=200,
    )

    assert TamaraProvider().verify(_stub_order(), None) is False


@responses.activate
def test_verify_returns_false_for_new_status(tamara_settings):
    """Just-created orders are 'new' — not yet paid."""
    responses.add(
        responses.GET,
        f"{TAMARA_BASE}/orders/tamara-order-abc",
        json={"status": "new"},
        status=200,
    )

    assert TamaraProvider().verify(_stub_order(), None) is False


def test_verify_returns_false_when_provider_ref_missing(tamara_settings):
    order = MagicMock(provider_ref="")
    assert TamaraProvider().verify(order, None) is False


def test_verify_returns_false_when_settings_unconfigured(settings):
    settings.TAMARA_BASE_URL = ""
    settings.TAMARA_API_KEY = ""

    assert TamaraProvider().verify(_stub_order(), None) is False


@responses.activate
def test_verify_returns_false_on_5xx(tamara_settings):
    responses.add(
        responses.GET,
        f"{TAMARA_BASE}/orders/tamara-order-abc",
        json={"detail": "internal error"},
        status=500,
    )

    assert TamaraProvider().verify(_stub_order(), None) is False


# --------------------------------------------------------------------------- #
# Webhook view
# --------------------------------------------------------------------------- #

WEBHOOK_URL = "/api/v1/payments/webhook/tamara/"


def _signed_jwt(payload=None):
    return jwt.encode(payload or {}, TAMARA_NOTIFICATION_TOKEN, algorithm="HS256")


@pytest.mark.django_db
class TestTamaraWebhook:
    def _make_order(self, user, product):
        order = Order.objects.create(
            user=user,
            name="Test",
            email="t@example.com",
            phone="+971501234567",
            address_line1="123 Test",
            city="Dubai",
            currency="AED",
            subtotal=Decimal("100"),
            total=Decimal("100"),
            payment_method="tamara",
            provider="tamara",
            provider_ref="tamara-order-abc",
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            title=product.title,
            unit_price=product.price,
            quantity=1,
        )
        return order

    @responses.activate
    def test_valid_jwt_and_authorised_status_marks_order_paid(
        self, api_client, user, product, tamara_settings
    ):
        order = self._make_order(user, product)
        responses.add(
            responses.GET,
            f"{TAMARA_BASE}/orders/tamara-order-abc",
            json={"status": "authorised"},
            status=200,
        )

        response = api_client.post(
            WEBHOOK_URL,
            {"order_id": "tamara-order-abc", "event_type": "order_authorised"},
            HTTP_AUTHORIZATION=f"Bearer {_signed_jwt()}",
            format="json",
        )

        assert response.status_code == 200
        order.refresh_from_db()
        assert order.paid is True
        assert order.status == Order.Status.PAID

    def test_invalid_jwt_returns_401(self, api_client, tamara_settings):
        response = api_client.post(
            WEBHOOK_URL,
            {"order_id": "tamara-order-abc"},
            HTTP_AUTHORIZATION="Bearer not-a-real-jwt",
            format="json",
        )

        assert response.status_code == 401

    def test_missing_jwt_returns_401(self, api_client, tamara_settings):
        response = api_client.post(
            WEBHOOK_URL,
            {"order_id": "tamara-order-abc"},
            format="json",
        )

        assert response.status_code == 401

    def test_unknown_order_returns_404(self, api_client, tamara_settings):
        response = api_client.post(
            WEBHOOK_URL,
            {"order_id": "ghost-order-xyz"},
            HTTP_AUTHORIZATION=f"Bearer {_signed_jwt()}",
            format="json",
        )

        assert response.status_code == 404

    @responses.activate
    def test_when_upstream_status_not_paid_does_not_mark_paid(
        self, api_client, user, product, tamara_settings
    ):
        order = self._make_order(user, product)
        responses.add(
            responses.GET,
            f"{TAMARA_BASE}/orders/tamara-order-abc",
            json={"status": "declined"},
            status=200,
        )

        response = api_client.post(
            WEBHOOK_URL,
            {"order_id": "tamara-order-abc"},
            HTTP_AUTHORIZATION=f"Bearer {_signed_jwt()}",
            format="json",
        )

        assert response.status_code == 200  # we ack the webhook either way
        order.refresh_from_db()
        assert order.paid is False
        assert order.status == Order.Status.PENDING

    @responses.activate
    def test_idempotent_when_order_already_paid(self, api_client, user, product, tamara_settings):
        order = self._make_order(user, product)
        order.paid = True
        order.status = Order.Status.PAID
        order.save(update_fields=["paid", "status"])
        starting_stock = product.stock

        responses.add(
            responses.GET,
            f"{TAMARA_BASE}/orders/tamara-order-abc",
            json={"status": "authorised"},
            status=200,
        )

        api_client.post(
            WEBHOOK_URL,
            {"order_id": "tamara-order-abc"},
            HTTP_AUTHORIZATION=f"Bearer {_signed_jwt()}",
            format="json",
        )

        # Stock should not be decremented twice — _apply_payment short-circuits
        product.refresh_from_db()
        assert product.stock == starting_stock
