"""
Seed everything needed for an end-to-end demo:
- Catalog (delegates to `seed_demo`)
- Repair services (delegates to `seed_repairs`)
- Realistic reviews (8-12 different reviewers, varied ratings, random spread)
- Demo customer + admin user with default addresses
- A handful of sample orders across different statuses
- A handful of sample repair bookings across different statuses

Idempotent — safe to re-run.
"""

import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.accounts.models import Address
from apps.catalog.models import Product, Review
from apps.orders.models import Order, OrderItem
from apps.repairs.models import RepairBooking, RepairService

User = get_user_model()

REVIEWS = [
    ("Ahmed K.", 5, "Exactly as described — arrived next day. Would buy again."),
    ("Fatima S.", 5, "Great service and fast delivery to Sharjah. Packaged well."),
    ("Mohammed A.", 4, "Good product but came a day late. Still recommend."),
    ("Layla H.", 5, "Perfect condition, sealed box, best price in UAE."),
    ("Omar R.", 5, "Honest shop, good warranty, trustworthy."),
    ("Zara M.", 4, "Exactly what I expected. Price is fair."),
    ("Hassan T.", 5, "Tried Tamara, approval was instant. Very smooth checkout."),
    ("Aisha N.", 5, "Called for repair quote — they picked up within seconds."),
    ("Khalid B.", 4, "Solid product. Came with all accessories. Recommended."),
    ("Noura Z.", 5, "Genuine product, came sealed. Customer service was excellent."),
    ("Yousef A.", 5, "Best price I found in Sharjah. Will come again."),
    ("Mariam K.", 4, "Very happy with the purchase. Delivery was same day."),
    ("Saleh M.", 5, "Quality product, exactly as advertised. 5 stars."),
    ("Reem H.", 5, "Trade-in value was fair. Smooth process."),
    ("Tariq F.", 4, "Good experience overall. Slight delay but worth it."),
    ("Hessa A.", 5, "Highly recommend — they explain everything clearly."),
]

REPAIR_BOOKINGS = [
    {
        "service_name": "iPhone Screen Replacement",
        "name": "Yousef Al Marzooqi",
        "phone": "+971501234567",
        "device_brand": "Apple",
        "device_model": "iPhone 14 Pro",
        "issue": "Top-right corner cracked, touch unresponsive in that area. Dropped from waist height.",
        "status": "ready",
        "quoted_price": "299.00",
    },
    {
        "service_name": "Phone Battery Replacement",
        "name": "Mariam Khalifa",
        "phone": "+971502345678",
        "device_brand": "Apple",
        "device_model": "iPhone 12",
        "issue": "Battery health 78%, dies by mid-day. Phone is just over 2 years old.",
        "status": "completed",
        "quoted_price": "149.00",
    },
    {
        "service_name": "Laptop Screen Replacement",
        "name": "Ahmed Saif",
        "phone": "+971503456789",
        "device_brand": "Apple",
        "device_model": "MacBook Air M2",
        "issue": "Stepped on closed laptop. Bottom-left of screen cracked, top still works fine.",
        "status": "in_progress",
        "quoted_price": "899.00",
    },
    {
        "service_name": "Liquid Spill Recovery",
        "name": "Hessa Al Suwaidi",
        "phone": "+971504567890",
        "device_brand": "Dell",
        "device_model": "XPS 13 (2022)",
        "issue": "Coffee spill on keyboard 24 hours ago. Won't power on. Important work files inside.",
        "status": "quoted",
        "quoted_price": "349.00",
    },
    {
        "service_name": "Android Screen Replacement",
        "name": "Tariq Hamdan",
        "phone": "+971505678901",
        "device_brand": "Samsung",
        "device_model": "Galaxy S23 Ultra",
        "issue": "Long crack across the front. Phone still works, just want it fixed.",
        "status": "requested",
        "quoted_price": None,
    },
]


class Command(BaseCommand):
    help = "Seed an end-to-end demo: catalog + services + users + orders + bookings."

    def handle(self, *args, **options):
        self.stdout.write(">>Catalog ...")
        call_command("seed_demo")

        self.stdout.write(">>Repair services ...")
        call_command("seed_repairs")

        self.stdout.write(">>Reviews ...")
        random.seed(42)
        for product in Product.objects.all():
            existing = product.reviews.count()
            target = random.randint(2, 5)
            for _ in range(max(0, target - existing)):
                user, rating, text = random.choice(REVIEWS)
                Review.objects.create(product=product, user=user, rating=rating, text=text)

        self.stdout.write(">>Demo customer + admin ...")
        demo, demo_created = User.objects.get_or_create(
            email="demo@shahzad.ae",
            defaults={
                "username": "demo@shahzad.ae",
                "first_name": "Demo",
                "last_name": "User",
            },
        )
        if demo_created or not demo.has_usable_password():
            demo.set_password("Demo1234!")
            demo.save()

        Address.objects.get_or_create(
            user=demo,
            address_line1="Rolla Square, Al Wahda St",
            defaults={
                "name": "Demo User",
                "phone": "+971501234567",
                "email": demo.email,
                "city": "Sharjah",
                "postal_code": "00000",
                "country": "UAE",
                "is_default": True,
            },
        )

        admin, admin_created = User.objects.get_or_create(
            email="admin@shahzad.ae",
            defaults={
                "username": "admin@shahzad.ae",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if admin_created:
            admin.set_password("Admin1234!")
            admin.save()

        self.stdout.write(">>Sample orders ...")
        self._seed_orders(demo)

        self.stdout.write(">>Sample repair bookings ...")
        self._seed_repair_bookings()

        self.stdout.write(
            self.style.SUCCESS(
                "\nDemo data ready:\n"
                f"  Products:        {Product.objects.count()}\n"
                f"  Reviews:         {Review.objects.count()}\n"
                f"  Repair services: {RepairService.objects.count()}\n"
                f"  Repair bookings: {RepairBooking.objects.count()}\n"
                f"  Users:           {User.objects.count()}\n"
                f"  Orders:          {Order.objects.count()}\n"
                "\nLogin credentials:\n"
                "  Customer: demo@shahzad.ae   / Demo1234!\n"
                "  Admin:    admin@shahzad.ae  / Admin1234!  (/admin/)\n"
            )
        )

    def _seed_orders(self, demo):
        if Order.objects.filter(user=demo).count() >= 3:
            return  # already seeded
        products = list(Product.objects.filter(stock__gt=0).order_by("?")[:20])
        if not products:
            return

        scenarios = [
            ("paid", "tamara", True, 1),
            ("delivered", "cod", True, 2),
            ("shipped", "tabby", True, 3),
            ("pending", "cod", False, 1),
        ]
        for status, method, paid, count in scenarios:
            picks = random.sample(products, k=min(count, len(products)))
            subtotal = sum((p.price for p in picks), Decimal("0"))
            order = Order.objects.create(
                user=demo,
                name="Demo User",
                email=demo.email,
                phone="+971501234567",
                address_line1="Rolla Square, Al Wahda St",
                city="Sharjah",
                postal_code="00000",
                country="UAE",
                currency="AED",
                subtotal=subtotal,
                total=subtotal,
                payment_method=method,
                provider=method,
                status=status,
                paid=paid,
            )
            for p in picks:
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    title=p.title,
                    unit_price=p.price,
                    quantity=1,
                    image=p.primary_image,
                )

    def _seed_repair_bookings(self):
        if RepairBooking.objects.count() >= 3:
            return  # already seeded
        for b in REPAIR_BOOKINGS:
            service = RepairService.objects.filter(name=b["service_name"]).first()
            email_local = b["name"].split()[0].lower().replace(" ", "")
            RepairBooking.objects.create(
                service=service,
                name=b["name"],
                email=f"{email_local}@example.com",
                phone=b["phone"],
                device_brand=b["device_brand"],
                device_model=b["device_model"],
                issue=b["issue"],
                status=b["status"],
                quoted_price=Decimal(b["quoted_price"]) if b["quoted_price"] else None,
            )
