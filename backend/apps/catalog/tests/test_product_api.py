"""Tests for the catalog product API: list, search, filter, sort, detail."""

import pytest


@pytest.mark.django_db
class TestProductList:
    def test_list_returns_only_active_products(self, api_client, brand):
        from conftest import ProductFactory

        active1 = ProductFactory(brand=brand, category=brand.category, is_active=True)
        active2 = ProductFactory(brand=brand, category=brand.category, is_active=True)
        ProductFactory(brand=brand, category=brand.category, is_active=False)

        response = api_client.get("/api/v1/catalog/products/")

        assert response.status_code == 200
        titles = [p["title"] for p in response.data["results"]]
        assert active1.title in titles
        assert active2.title in titles
        assert len(response.data["results"]) == 2

    def test_response_is_paginated(self, api_client, product):
        response = api_client.get("/api/v1/catalog/products/")

        assert "results" in response.data
        assert "count" in response.data


@pytest.mark.django_db
class TestProductSearch:
    def test_q_param_matches_title_substring(self, api_client, brand):
        from conftest import ProductFactory

        match = ProductFactory(brand=brand, category=brand.category, title="iPhone 15 Pro Max")
        ProductFactory(brand=brand, category=brand.category, title="MacBook Air")

        response = api_client.get("/api/v1/catalog/products/?q=iPhone")

        titles = [p["title"] for p in response.data["results"]]
        assert match.title in titles
        assert "MacBook Air" not in titles

    def test_q_param_is_case_insensitive(self, api_client, brand):
        from conftest import ProductFactory

        ProductFactory(brand=brand, category=brand.category, title="Galaxy S24 Ultra")

        response = api_client.get("/api/v1/catalog/products/?q=galaxy")

        assert len(response.data["results"]) == 1


@pytest.mark.django_db
class TestProductSort:
    """Both `?sort=` (legacy, used by the storefront) and `?ordering=` (DRF native) work."""

    def test_ordering_price_asc(self, api_client, brand):
        from decimal import Decimal

        from conftest import ProductFactory

        ProductFactory(brand=brand, category=brand.category, price=Decimal("500"))
        ProductFactory(brand=brand, category=brand.category, price=Decimal("100"))
        ProductFactory(brand=brand, category=brand.category, price=Decimal("250"))

        response = api_client.get("/api/v1/catalog/products/?ordering=price")
        prices = [float(p["price"]) for p in response.data["results"]]

        assert prices == sorted(prices)

    def test_ordering_price_desc(self, api_client, brand):
        from decimal import Decimal

        from conftest import ProductFactory

        ProductFactory(brand=brand, category=brand.category, price=Decimal("500"))
        ProductFactory(brand=brand, category=brand.category, price=Decimal("100"))

        response = api_client.get("/api/v1/catalog/products/?ordering=-price")
        prices = [float(p["price"]) for p in response.data["results"]]

        assert prices == sorted(prices, reverse=True)

    def test_legacy_sort_param_works_too(self, api_client, brand):
        """Storefront uses ?sort=price_asc historically — verify it works post-fix."""
        from decimal import Decimal

        from conftest import ProductFactory

        ProductFactory(brand=brand, category=brand.category, price=Decimal("500"))
        ProductFactory(brand=brand, category=brand.category, price=Decimal("100"))
        ProductFactory(brand=brand, category=brand.category, price=Decimal("250"))

        response = api_client.get("/api/v1/catalog/products/?sort=price_asc")
        prices = [float(p["price"]) for p in response.data["results"]]

        assert prices == sorted(prices)


@pytest.mark.django_db
class TestProductFilter:
    def test_filter_by_featured(self, api_client, brand):
        from conftest import ProductFactory

        featured = ProductFactory(brand=brand, category=brand.category, is_featured=True)
        ProductFactory(brand=brand, category=brand.category, is_featured=False)

        response = api_client.get("/api/v1/catalog/products/?is_featured=true")

        titles = [p["title"] for p in response.data["results"]]
        assert featured.title in titles
        assert len(response.data["results"]) == 1


@pytest.mark.django_db
class TestProductDetail:
    def test_retrieve_by_slug(self, api_client, product):
        response = api_client.get(f"/api/v1/catalog/products/{product.slug}/")

        assert response.status_code == 200
        assert response.data["title"] == product.title

    def test_inactive_product_404s(self, api_client, brand):
        from conftest import ProductFactory

        inactive = ProductFactory(brand=brand, category=brand.category, is_active=False)

        response = api_client.get(f"/api/v1/catalog/products/{inactive.slug}/")

        assert response.status_code == 404

    def test_unknown_slug_404s(self, api_client):
        response = api_client.get("/api/v1/catalog/products/nope-not-a-product/")

        assert response.status_code == 404
