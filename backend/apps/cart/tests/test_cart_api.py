"""Tests for the cart API: add, update, remove, clear, guest, merge."""
import pytest

from apps.cart.models import Cart, CartItem


@pytest.mark.django_db
class TestCartAdd:
    def test_authenticated_user_can_add_item(self, auth_api_client, user, product):
        response = auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk})

        assert response.status_code == 200
        cart = Cart.objects.get(user=user)
        assert cart.items.count() == 1
        assert cart.items.first().quantity == 1

    def test_adding_same_item_twice_merges_quantity(self, auth_api_client, user, product):
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk, "quantity": 2})
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk, "quantity": 3})

        cart = Cart.objects.get(user=user)
        assert cart.items.count() == 1
        assert cart.items.first().quantity == 5

    def test_adding_nonexistent_product_returns_404(self, auth_api_client):
        response = auth_api_client.post("/api/v1/cart/add/", {"product_id": 999_999})

        assert response.status_code == 404

    def test_quantity_defaults_to_one_when_omitted(self, auth_api_client, user, product):
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk})

        item = Cart.objects.get(user=user).items.first()
        assert item.quantity == 1


@pytest.mark.django_db
class TestCartItemMutations:
    def test_patch_updates_quantity(self, auth_api_client, user, product):
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk})
        item = CartItem.objects.get(cart__user=user)

        response = auth_api_client.patch(f"/api/v1/cart/items/{item.pk}/", {"quantity": 7})

        assert response.status_code == 200
        item.refresh_from_db()
        assert item.quantity == 7

    def test_patch_to_zero_removes_item(self, auth_api_client, user, product):
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk})
        item = CartItem.objects.get(cart__user=user)

        auth_api_client.patch(f"/api/v1/cart/items/{item.pk}/", {"quantity": 0})

        assert not CartItem.objects.filter(pk=item.pk).exists()

    def test_delete_removes_item(self, auth_api_client, user, product):
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk})
        item = CartItem.objects.get(cart__user=user)

        response = auth_api_client.delete(f"/api/v1/cart/items/{item.pk}/")

        assert response.status_code == 200
        assert not CartItem.objects.filter(pk=item.pk).exists()

    def test_clear_removes_all_items(self, auth_api_client, user, product, brand):
        from conftest import ProductFactory

        product2 = ProductFactory(brand=brand, category=brand.category)
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product.pk})
        auth_api_client.post("/api/v1/cart/add/", {"product_id": product2.pk})
        assert CartItem.objects.filter(cart__user=user).count() == 2

        response = auth_api_client.post("/api/v1/cart/clear/")

        assert response.status_code == 200
        assert CartItem.objects.filter(cart__user=user).count() == 0


@pytest.mark.django_db
class TestGuestCart:
    SESSION_KEY = "test-guest-abc-123"

    def test_guest_can_add_item_via_session_header(self, api_client, product):
        response = api_client.post(
            "/api/v1/cart/add/",
            {"product_id": product.pk},
            HTTP_X_GUEST_SESSION=self.SESSION_KEY,
        )

        assert response.status_code == 200
        cart = Cart.objects.get(session_key=self.SESSION_KEY)
        assert cart.user is None
        assert cart.items.count() == 1

    def test_guest_without_session_header_is_rejected(self, api_client, product):
        response = api_client.post("/api/v1/cart/add/", {"product_id": product.pk})

        assert response.status_code == 400


@pytest.mark.django_db
class TestCartMerge:
    SESSION_KEY = "merge-test-key"

    def test_merge_moves_guest_items_into_user_cart(
        self, api_client, auth_api_client, user, product
    ):
        # Step 1 — guest adds an item via session header
        api_client.post(
            "/api/v1/cart/add/",
            {"product_id": product.pk, "quantity": 2},
            HTTP_X_GUEST_SESSION=self.SESSION_KEY,
        )
        assert Cart.objects.get(session_key=self.SESSION_KEY).items.count() == 1

        # Step 2 — same guest "logs in" and triggers merge
        response = auth_api_client.post(
            "/api/v1/cart/merge/",
            {"session_key": self.SESSION_KEY},
        )

        assert response.status_code == 200
        user_cart = Cart.objects.get(user=user)
        assert user_cart.items.count() == 1
        assert user_cart.items.first().quantity == 2
