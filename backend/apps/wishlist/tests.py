"""
Wishlist API tests.

Coverage:
  - Auth enforcement (401 for anon on every endpoint)
  - User scoping (user A cannot read / remove user B's entries)
  - Duplicate prevention (POST + toggle are idempotent)
  - Toggle correctness (add then remove)
  - Check probe returns booleans
  - 404 for missing/inactive products
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Category, Product
from apps.wishlist.models import WishedProduct

User = get_user_model()


class WishlistAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice = User.objects.create_user(username="alice", email="alice@test.com", password="pw")
        cls.bob = User.objects.create_user(username="bob", email="bob@test.com", password="pw")
        cls.cat = Category.objects.create(name="Phones", slug="phones")
        cls.p1 = Product.objects.create(title="iPhone 15", slug="iphone-15", price=3000, category=cls.cat, is_active=True)
        cls.p2 = Product.objects.create(title="Pixel 9", slug="pixel-9", price=2500, category=cls.cat, is_active=True)
        cls.inactive = Product.objects.create(title="Old Phone", slug="old-phone", price=100, category=cls.cat, is_active=False)

    # ── auth ──────────────────────────────────────────────────────
    def test_anon_cannot_list(self):
        r = self.client.get("/api/v1/wishlist/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_cannot_add(self):
        r = self.client.post("/api/v1/wishlist/", {"product_id": self.p1.id}, format="json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_cannot_toggle(self):
        r = self.client.post(f"/api/v1/wishlist/toggle/{self.p1.id}/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anon_cannot_check(self):
        r = self.client.get(f"/api/v1/wishlist/check/{self.p1.id}/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── list ──────────────────────────────────────────────────────
    def test_list_returns_only_current_users_entries(self):
        WishedProduct.objects.create(user=self.alice, product=self.p1)
        WishedProduct.objects.create(user=self.bob, product=self.p2)
        self.client.force_authenticate(self.alice)
        r = self.client.get("/api/v1/wishlist/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)
        self.assertEqual(r.data[0]["product"]["id"], self.p1.id)

    # ── add / dup prevention ──────────────────────────────────────
    def test_add_creates_entry(self):
        self.client.force_authenticate(self.alice)
        r = self.client.post("/api/v1/wishlist/", {"product_id": self.p1.id}, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertTrue(WishedProduct.objects.filter(user=self.alice, product=self.p1).exists())

    def test_add_is_idempotent(self):
        self.client.force_authenticate(self.alice)
        self.client.post("/api/v1/wishlist/", {"product_id": self.p1.id}, format="json")
        r = self.client.post("/api/v1/wishlist/", {"product_id": self.p1.id}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(WishedProduct.objects.filter(user=self.alice, product=self.p1).count(), 1)

    def test_add_requires_product_id(self):
        self.client.force_authenticate(self.alice)
        r = self.client.post("/api/v1/wishlist/", {}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_rejects_inactive_product(self):
        self.client.force_authenticate(self.alice)
        r = self.client.post("/api/v1/wishlist/", {"product_id": self.inactive.id}, format="json")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    # ── remove ────────────────────────────────────────────────────
    def test_remove_deletes_entry(self):
        WishedProduct.objects.create(user=self.alice, product=self.p1)
        self.client.force_authenticate(self.alice)
        r = self.client.delete(f"/api/v1/wishlist/{self.p1.id}/")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WishedProduct.objects.filter(user=self.alice, product=self.p1).exists())

    def test_remove_returns_404_if_not_in_list(self):
        self.client.force_authenticate(self.alice)
        r = self.client.delete(f"/api/v1/wishlist/{self.p1.id}/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_cannot_delete_another_users_entry(self):
        WishedProduct.objects.create(user=self.bob, product=self.p1)
        self.client.force_authenticate(self.alice)
        r = self.client.delete(f"/api/v1/wishlist/{self.p1.id}/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        # Bob's entry must still be intact.
        self.assertTrue(WishedProduct.objects.filter(user=self.bob, product=self.p1).exists())

    # ── toggle ────────────────────────────────────────────────────
    def test_toggle_adds_then_removes(self):
        self.client.force_authenticate(self.alice)
        r1 = self.client.post(f"/api/v1/wishlist/toggle/{self.p1.id}/")
        self.assertEqual(r1.status_code, 200)
        self.assertTrue(r1.data["in_wishlist"])
        r2 = self.client.post(f"/api/v1/wishlist/toggle/{self.p1.id}/")
        self.assertFalse(r2.data["in_wishlist"])
        self.assertFalse(WishedProduct.objects.filter(user=self.alice, product=self.p1).exists())

    # ── check ─────────────────────────────────────────────────────
    def test_check_reports_status(self):
        self.client.force_authenticate(self.alice)
        r = self.client.get(f"/api/v1/wishlist/check/{self.p1.id}/")
        self.assertFalse(r.data["in_wishlist"])
        WishedProduct.objects.create(user=self.alice, product=self.p1)
        r = self.client.get(f"/api/v1/wishlist/check/{self.p1.id}/")
        self.assertTrue(r.data["in_wishlist"])

    def test_check_is_user_scoped(self):
        WishedProduct.objects.create(user=self.bob, product=self.p1)
        self.client.force_authenticate(self.alice)
        r = self.client.get(f"/api/v1/wishlist/check/{self.p1.id}/")
        self.assertFalse(r.data["in_wishlist"])  # Alice shouldn't see Bob's state
