"""
Sanity check for the stock-decrement race-condition fix.

Spawns two threads that try to decrement stock on the same product (each via
its own Order, qty=1 against initial stock=1). With the row lock in place,
exactly ONE thread should succeed and the OTHER should raise ValidationError,
leaving final stock at 0 (no overselling).

Usage:
    python manage.py check_stock_race

Requirements:
    - Local Postgres reachable via your settings (works against the dev DB).
    - Migrations applied. Creates a hidden test category + product
      (slugs prefixed with "__race-test"), cleans up its orders on exit.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import close_old_connections, transaction
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem
from apps.payments.api.views import _decrement_stock

CATEGORY_SLUG = "__race-test-category__"
PRODUCT_SLUG = "__race-test-product__"


class Command(BaseCommand):
    help = "Verify that concurrent stock decrements do not oversell."

    def handle(self, *args, **options):
        product = self._setup_product()
        orders = self._setup_orders(product)

        try:
            results = self._run_concurrent(orders)
            product.refresh_from_db()
            self._report(results, product)
        finally:
            for o in orders:
                o.items.all().delete()
                o.delete()

    def _setup_product(self):
        category, _ = Category.objects.get_or_create(
            slug=CATEGORY_SLUG,
            defaults={"name": "Race Test", "is_active": False},
        )
        product, _ = Product.objects.get_or_create(
            slug=PRODUCT_SLUG,
            defaults={
                "title": "Race Test Product",
                "category": category,
                "price": Decimal("10.00"),
                "stock": 1,
                "is_active": False,
            },
        )
        Product.objects.filter(pk=product.pk).update(stock=1)
        product.refresh_from_db()
        self.stdout.write(f"Test product ready: id={product.pk} stock={product.stock}")
        return product

    def _setup_orders(self, product):
        orders = []
        for i in range(2):
            order = Order.objects.create(
                name=f"Race test {i}",
                email=f"race{i}@example.com",
                address_line1="123 Test",
                city="Dubai",
                subtotal=Decimal("10.00"),
                total=Decimal("10.00"),
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                title=product.title,
                unit_price=product.price,
                quantity=1,
            )
            orders.append(order)
        return orders

    @staticmethod
    def _attempt(order_pk):
        close_old_connections()
        try:
            with transaction.atomic():
                order = Order.objects.get(pk=order_pk)
                _decrement_stock(order)
            return ("OK", order_pk, "")
        except DRFValidationError as exc:
            return ("VALIDATION", order_pk, str(exc.detail))
        except Exception as exc:
            return ("ERROR", order_pk, repr(exc))

    def _run_concurrent(self, orders):
        with ThreadPoolExecutor(max_workers=2) as ex:
            futures = [ex.submit(self._attempt, o.pk) for o in orders]
            return [f.result() for f in as_completed(futures)]

    def _report(self, results, product):
        self.stdout.write("\nThread results:")
        for r in results:
            self.stdout.write(f"  {r}")
        self.stdout.write(f"Final product stock: {product.stock}")

        oks = [r for r in results if r[0] == "OK"]
        validations = [r for r in results if r[0] == "VALIDATION"]
        errors = [r for r in results if r[0] == "ERROR"]

        if len(oks) == 1 and len(validations) == 1 and not errors and product.stock == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "\nPASS: lock prevented overselling — exactly one order succeeded, stock=0."
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    "\nFAIL: expected 1 OK + 1 VALIDATION with stock=0; got "
                    f"{len(oks)} OK, {len(validations)} VALIDATION, {len(errors)} ERROR, stock={product.stock}."
                )
            )
