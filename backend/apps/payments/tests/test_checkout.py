"""Tests for the COD checkout flow at POST /api/v1/payments/checkout/."""

import pytest

from apps.cart.models import Cart, CartItem
from apps.orders.models import Order


def _checkout_payload(**overrides):
    base = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "+971501234567",
        "address_line1": "123 Test Street",
        "city": "Dubai",
        "country": "UAE",
        "payment_method": "cod",
    }
    base.update(overrides)
    return base


@pytest.mark.django_db
class TestCheckoutHappyPath:
    def test_creates_order_with_correct_user_and_total(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)

        response = auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        assert response.status_code == 201
        order = Order.objects.get(user=user)
        assert order.subtotal == product.price * 2
        assert order.shipping_fee == 30  # default UAE shipping
        assert order.bnpl_surcharge == 0  # COD has no surcharge
        assert order.total == product.price * 2 + 30
        assert order.payment_method == "cod"
        assert order.region == "UAE"
        assert order.email == "test@example.com"
        assert "reference" in response.data

    def test_creates_order_items_for_every_cart_line(self, auth_api_client, user, product, brand):
        from conftest import ProductFactory

        product2 = ProductFactory(brand=brand, category=brand.category, price="50.00")
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        CartItem.objects.create(cart=cart, product=product2, quantity=3)

        auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        order = Order.objects.get(user=user)
        assert order.items.count() == 2

    def test_clears_the_cart_after_successful_checkout(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        assert CartItem.objects.filter(cart=cart).count() == 0

    def test_decrements_stock_for_cod(self, auth_api_client, user, product):
        starting_stock = product.stock
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=3)

        auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        product.refresh_from_db()
        assert product.stock == starting_stock - 3


@pytest.mark.django_db
class TestCheckoutValidation:
    def test_rejects_empty_cart(self, auth_api_client, user):
        response = auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        assert response.status_code == 400
        assert "cart" in response.data["detail"].lower()

    def test_rejects_when_no_cart_exists_at_all(self, auth_api_client, user):
        response = auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        assert response.status_code == 400

    def test_rejects_invalid_payment_method(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        response = auth_api_client.post(
            "/api/v1/payments/checkout/",
            _checkout_payload(payment_method="bitcoin"),
        )

        assert response.status_code == 400

    def test_rejects_missing_required_address_fields(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        payload = _checkout_payload()
        del payload["address_line1"]
        response = auth_api_client.post("/api/v1/payments/checkout/", payload)

        assert response.status_code == 400


@pytest.mark.django_db
class TestCheckoutStockSafety:
    def test_rejects_when_stock_is_insufficient(self, auth_api_client, user, brand):
        from conftest import ProductFactory

        # Only 2 units in stock — try to buy 5
        scarce_product = ProductFactory(brand=brand, category=brand.category, stock=2)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=scarce_product, quantity=5)

        response = auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        assert response.status_code == 400
        # Order should NOT have been created (transaction rolled back)
        assert Order.objects.filter(user=user).count() == 0
        # Stock should be unchanged
        scarce_product.refresh_from_db()
        assert scarce_product.stock == 2

    def test_succeeds_when_stock_exactly_matches_quantity(self, auth_api_client, user, brand):
        from conftest import ProductFactory

        product = ProductFactory(brand=brand, category=brand.category, stock=2)
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)

        response = auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        assert response.status_code == 201
        product.refresh_from_db()
        assert product.stock == 0


@pytest.mark.django_db
class TestCheckoutRegionAndFees:
    """Region-specific shipping + 9% BNPL surcharge on subtotal."""

    def test_uae_default_charges_30_shipping(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload(region="UAE"))

        order = Order.objects.get(user=user)
        assert order.region == "UAE"
        assert order.shipping_fee == 30
        assert order.total == product.price + 30  # 100 + 30

    def test_ksa_charges_150_shipping_to_jeddah(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        auth_api_client.post(
            "/api/v1/payments/checkout/",
            _checkout_payload(region="KSA", city="Jeddah"),
        )

        order = Order.objects.get(user=user)
        assert order.region == "KSA"
        assert order.shipping_fee == 150
        assert order.total == product.price + 150

    def test_ksa_rejects_unsupported_city(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        response = auth_api_client.post(
            "/api/v1/payments/checkout/",
            _checkout_payload(region="KSA", city="Riyadh"),
        )

        assert response.status_code == 400
        assert "city" in response.data
        # No order should have been created on rejection
        assert Order.objects.filter(user=user).count() == 0

    def test_ksa_accepts_mecca_madina_jeddah(self, auth_api_client, user, brand):
        from conftest import ProductFactory

        for city in ["Mecca", "Madina", "Jeddah"]:
            user.orders.all().delete()
            p = ProductFactory(brand=brand, category=brand.category, price="100.00")
            cart, _ = Cart.objects.get_or_create(user=user)
            cart.items.all().delete()
            CartItem.objects.create(cart=cart, product=p, quantity=1)
            response = auth_api_client.post(
                "/api/v1/payments/checkout/",
                _checkout_payload(region="KSA", city=city),
            )
            assert response.status_code == 201, f"city={city} unexpectedly rejected"

    def test_tamara_adds_9pct_surcharge_on_subtotal(self, auth_api_client, user, product, settings):
        # Disable Tamara API call so we don't try to hit the network
        settings.TAMARA_BASE_URL = ""
        settings.TAMARA_API_KEY = ""
        settings.TAMARA_API_KEY_UAE = ""
        settings.TAMARA_API_KEY_KSA = ""
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)

        auth_api_client.post(
            "/api/v1/payments/checkout/",
            _checkout_payload(payment_method="tamara"),
        )

        order = Order.objects.get(user=user)
        # subtotal=200, surcharge=200*9%=18, shipping=30, total=248
        assert order.subtotal == 200
        assert order.bnpl_surcharge == 18
        assert order.shipping_fee == 30
        assert order.total == 248

    def test_tabby_adds_9pct_surcharge_on_subtotal(self, auth_api_client, user, product, settings):
        settings.TABBY_API_URL = ""
        settings.TABBY_SECRET_KEY = ""
        settings.TABBY_API_URL_UAE = ""
        settings.TABBY_SECRET_KEY_UAE = ""
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        auth_api_client.post(
            "/api/v1/payments/checkout/",
            _checkout_payload(payment_method="tabby"),
        )

        order = Order.objects.get(user=user)
        assert order.bnpl_surcharge == 9  # 100 * 9% = 9
        assert order.total == 100 + 30 + 9  # subtotal + shipping + surcharge

    def test_cod_has_no_bnpl_surcharge(self, auth_api_client, user, product):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        auth_api_client.post("/api/v1/payments/checkout/", _checkout_payload())

        order = Order.objects.get(user=user)
        assert order.bnpl_surcharge == 0


@pytest.mark.django_db
class TestGuestCheckout:
    SESSION_KEY = "checkout-guest-key"

    def test_guest_can_checkout_via_session_header(self, api_client, product):
        # Build the guest cart
        api_client.post(
            "/api/v1/cart/add/",
            {"product_id": product.pk},
            HTTP_X_GUEST_SESSION=self.SESSION_KEY,
        )

        response = api_client.post(
            "/api/v1/payments/checkout/",
            _checkout_payload(),
            HTTP_X_GUEST_SESSION=self.SESSION_KEY,
        )

        assert response.status_code == 201
        order = Order.objects.get(reference=response.data["reference"])
        assert order.user is None  # guest order
        assert order.items.count() == 1
