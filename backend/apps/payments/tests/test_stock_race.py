"""
Concurrency test for the stock-decrement lock.

Two threads try to decrement stock on the same product (qty=1, stock=1) at
the same time. With `select_for_update` in place, exactly ONE thread should
succeed; the other should raise `ValidationError`. Final stock must be 0
(no overselling, no negative-stock).

This is the pytest port of the `check_stock_race` management command — the
manual verification that ran during the original Item 5 work.
"""

from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

import pytest
from django.db import close_old_connections, transaction
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.orders.models import Order, OrderItem
from apps.payments.api.views import _decrement_stock


def _attempt(order_pk):
    """Worker: try to decrement stock for the given order in its own tx."""
    close_old_connections()
    try:
        with transaction.atomic():
            order = Order.objects.get(pk=order_pk)
            _decrement_stock(order)
        return "OK"
    except DRFValidationError:
        return "VALIDATION"
    except Exception as exc:  # pragma: no cover — surfaces unexpected errors
        return f"ERROR:{exc!r}"


@pytest.mark.django_db(transaction=True)
def test_concurrent_decrement_does_not_oversell(brand):
    """Two threads, stock=1: exactly one wins, stock lands at 0."""
    from conftest import ProductFactory, UserFactory

    user = UserFactory()
    product = ProductFactory(brand=brand, category=brand.category, stock=1)

    orders = []
    for i in range(2):
        order = Order.objects.create(
            user=user,
            name=f"Race {i}",
            email=f"race{i}@example.com",
            phone="+971501234567",
            address_line1="123 Test",
            city="Dubai",
            subtotal=Decimal("100"),
            total=Decimal("100"),
        )
        OrderItem.objects.create(
            order=order,
            product=product,
            title=product.title,
            unit_price=product.price,
            quantity=1,
        )
        orders.append(order)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(_attempt, [o.pk for o in orders]))

    product.refresh_from_db()
    assert results.count("OK") == 1, f"expected 1 success, got {results}"
    assert results.count("VALIDATION") == 1, f"expected 1 validation, got {results}"
    assert product.stock == 0, f"final stock {product.stock} — overselling!"
