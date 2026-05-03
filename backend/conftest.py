"""
Shared pytest fixtures + factory-boy factories for the test suite.

Imported automatically by pytest in any subdir under `backend/`. New tests
should pull from these fixtures rather than building their own ad-hoc setup.
"""
from decimal import Decimal

import factory
import pytest
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.cart.models import Cart, CartItem
from apps.catalog.models import Brand, Category, Product
from apps.orders.models import Order, OrderItem


# --------------------------------------------------------------------------- #
# factory-boy factories
# --------------------------------------------------------------------------- #

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@test.com")
    username = factory.LazyAttribute(lambda obj: obj.email)
    first_name = "Test"
    last_name = "User"
    is_active = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        obj.set_password(extracted or "TestPass123!")
        if create:
            obj.save()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: f"Brand {n}")
    category = factory.SubFactory(CategoryFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Sequence(lambda n: f"Test Product {n}")
    description = "Test product description"
    price = Decimal("100.00")
    stock = 10
    is_active = True
    brand = factory.SubFactory(BrandFactory)
    category = factory.LazyAttribute(lambda obj: obj.brand.category)


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


class GuestCartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = None
    session_key = factory.Sequence(lambda n: f"guest-session-{n}")


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    name = "Test Customer"
    email = factory.LazyAttribute(lambda obj: obj.user.email if obj.user else "guest@test.com")
    phone = "+971501234567"
    address_line1 = "123 Test St"
    city = "Dubai"
    subtotal = Decimal("100.00")
    total = Decimal("100.00")
    payment_method = "cod"
    provider = "cod"


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    title = factory.LazyAttribute(lambda obj: obj.product.title)
    unit_price = factory.LazyAttribute(lambda obj: obj.product.price)
    quantity = 1


# --------------------------------------------------------------------------- #
# pytest fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture
def user(db):
    """A standard test user. Default password: `TestPass123!`."""
    return UserFactory()


@pytest.fixture
def api_client():
    """Bare DRF APIClient instance — no auth."""
    return APIClient()


@pytest.fixture
def auth_api_client(user):
    """A fresh APIClient pre-authed as `user` via JWT bearer.

    Independent of the `api_client` fixture — request both in the same test
    and you get two separate clients (one anon, one authed).
    """
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def category(db):
    return CategoryFactory()


@pytest.fixture
def brand(db, category):
    return BrandFactory(category=category)


@pytest.fixture
def product(db, brand):
    return ProductFactory(brand=brand, category=brand.category)


@pytest.fixture
def out_of_stock_product(db, brand):
    return ProductFactory(brand=brand, category=brand.category, stock=0)


@pytest.fixture
def cart(db, user):
    return CartFactory(user=user)


@pytest.fixture
def guest_cart(db):
    return GuestCartFactory()
