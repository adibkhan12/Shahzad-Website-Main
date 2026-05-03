"""
Golden tests for the Tabby payment provider.

Covers `TabbyProvider.verify()` (which calls `GET /api/v2/payments/{id}`)
and the `/api/v1/payments/webhook/tabby/` view (X-Webhook-Auth shared-secret +
defense-in-depth status check).

Mocked using `responses` so we test against the documented API contract
without needing real sandbox keys.
"""

from decimal import Decimal
from unittest.mock import MagicMock

import pytest
import responses

from apps.orders.models import Order, OrderItem
from apps.payments.providers.tabby import TabbyProvider

TABBY_BASE = "https://api.tabby.ai"
TABBY_SECRET_KEY = "sk_test_tabby_secret_xyz"
TABBY_WEBHOOK_SECRET = "shared-webhook-secret-abc"


@pytest.fixture
def tabby_settings(settings):
    settings.TABBY_API_URL = TABBY_BASE
    settings.TABBY_SECRET_KEY = TABBY_SECRET_KEY
    settings.TABBY_WEBHOOK_SECRET = TABBY_WEBHOOK_SECRET
    return settings


def _stub_order(ref="tabby-payment-abc"):
    return MagicMock(provider_ref=ref)


# --------------------------------------------------------------------------- #
# TabbyProvider.verify()
# --------------------------------------------------------------------------- #


@responses.activate
def test_verify_returns_true_for_authorized(tabby_settings):
    responses.add(
        responses.GET,
        f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
        json={"id": "tabby-payment-abc", "status": "AUTHORIZED"},
        status=200,
    )

    assert TabbyProvider().verify(_stub_order(), None) is True


@responses.activate
def test_verify_returns_true_for_closed(tabby_settings):
    responses.add(
        responses.GET,
        f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
        json={"status": "CLOSED"},
        status=200,
    )

    assert TabbyProvider().verify(_stub_order(), None) is True


@responses.activate
def test_verify_returns_false_for_rejected(tabby_settings):
    responses.add(
        responses.GET,
        f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
        json={"status": "REJECTED"},
        status=200,
    )

    assert TabbyProvider().verify(_stub_order(), None) is False


@responses.activate
def test_verify_returns_false_for_expired(tabby_settings):
    responses.add(
        responses.GET,
        f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
        json={"status": "EXPIRED"},
        status=200,
    )

    assert TabbyProvider().verify(_stub_order(), None) is False


@responses.activate
def test_verify_returns_false_for_created_status(tabby_settings):
    """`CREATED` is the pre-authorization state — customer hasn't paid yet."""
    responses.add(
        responses.GET,
        f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
        json={"status": "CREATED"},
        status=200,
    )

    assert TabbyProvider().verify(_stub_order(), None) is False


def test_verify_returns_false_when_provider_ref_missing(tabby_settings):
    order = MagicMock(provider_ref="")
    assert TabbyProvider().verify(order, None) is False


def test_verify_returns_false_when_settings_unconfigured(settings):
    settings.TABBY_API_URL = ""
    settings.TABBY_SECRET_KEY = ""

    assert TabbyProvider().verify(_stub_order(), None) is False


@responses.activate
def test_verify_returns_false_on_404(tabby_settings):
    responses.add(
        responses.GET,
        f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
        json={"detail": "not found"},
        status=404,
    )

    assert TabbyProvider().verify(_stub_order(), None) is False


# --------------------------------------------------------------------------- #
# Webhook view
# --------------------------------------------------------------------------- #

WEBHOOK_URL = "/api/v1/payments/webhook/tabby/"


@pytest.mark.django_db
class TestTabbyWebhook:
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
            payment_method="tabby",
            provider="tabby",
            provider_ref="tabby-payment-abc",
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
    def test_valid_secret_and_authorized_status_marks_order_paid(
        self, api_client, user, product, tabby_settings
    ):
        order = self._make_order(user, product)
        responses.add(
            responses.GET,
            f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
            json={"status": "AUTHORIZED"},
            status=200,
        )

        response = api_client.post(
            WEBHOOK_URL,
            {"id": "tabby-payment-abc", "status": "AUTHORIZED"},
            HTTP_X_WEBHOOK_AUTH=TABBY_WEBHOOK_SECRET,
            format="json",
        )

        assert response.status_code == 200
        order.refresh_from_db()
        assert order.paid is True
        assert order.status == Order.Status.PAID

    def test_invalid_secret_returns_401(self, api_client, tabby_settings):
        response = api_client.post(
            WEBHOOK_URL,
            {"id": "tabby-payment-abc"},
            HTTP_X_WEBHOOK_AUTH="wrong-secret",
            format="json",
        )

        assert response.status_code == 401

    def test_missing_secret_returns_401(self, api_client, tabby_settings):
        response = api_client.post(
            WEBHOOK_URL,
            {"id": "tabby-payment-abc"},
            format="json",
        )

        assert response.status_code == 401

    def test_unknown_payment_id_returns_404(self, api_client, tabby_settings):
        response = api_client.post(
            WEBHOOK_URL,
            {"id": "ghost-payment-xyz"},
            HTTP_X_WEBHOOK_AUTH=TABBY_WEBHOOK_SECRET,
            format="json",
        )

        assert response.status_code == 404

    @responses.activate
    def test_when_upstream_status_rejected_does_not_mark_paid(
        self, api_client, user, product, tabby_settings
    ):
        order = self._make_order(user, product)
        responses.add(
            responses.GET,
            f"{TABBY_BASE}/api/v2/payments/tabby-payment-abc",
            json={"status": "REJECTED"},
            status=200,
        )

        response = api_client.post(
            WEBHOOK_URL,
            {"id": "tabby-payment-abc"},
            HTTP_X_WEBHOOK_AUTH=TABBY_WEBHOOK_SECRET,
            format="json",
        )

        assert response.status_code == 200
        order.refresh_from_db()
        assert order.paid is False


def test_unknown_provider_returns_404(api_client):
    response = api_client.post("/api/v1/payments/webhook/stripe/", {})
    assert response.status_code == 404
