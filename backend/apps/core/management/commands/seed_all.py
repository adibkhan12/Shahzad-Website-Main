import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.accounts.models import Address
from apps.catalog.models import Product, Review
from apps.orders.models import Order, OrderItem
from apps.repairs.models import RepairService

User = get_user_model()


REPAIR_SERVICES = [
    ("iPhone screen replacement", "phone", "Fast same-day replacement with genuine-quality OLED.", 449, 45, "📱", True, 1),
    ("iPhone battery replacement", "phone", "Restore 100% battery health in under 30 minutes.", 199, 30, "🔋", True, 2),
    ("Android screen replacement", "phone", "Samsung, Xiaomi, OnePlus and more.", 349, 60, "📱", False, 3),
    ("Water damage diagnosis", "phone", "Ultrasonic cleaning + recovery attempt.", 249, 120, "💧", False, 4),
    ("MacBook battery swap", "laptop", "Apple-grade replacement batteries, 1-year warranty.", 699, 90, "💻", True, 5),
    ("Laptop keyboard replacement", "laptop", "Full keyboard swap for most makes and models.", 449, 90, "⌨️", False, 6),
    ("Laptop SSD upgrade", "laptop", "Upgrade to 1TB/2TB NVMe with data migration.", 549, 60, "💾", False, 7),
    ("iPad screen replacement", "tablet", "iPad Pro, Air, and Mini glass replacement.", 499, 90, "📟", False, 8),
    ("Apple Watch screen", "watch", "Display replacement for all Apple Watch series.", 399, 75, "⌚", False, 9),
    ("Data recovery", "other", "Recover data from dead phones, laptops, drives.", 299, 240, "🛟", False, 10),
]


REVIEWS = [
    ("Ahmed K.", 5, "Exactly as described — arrived next day. Would buy again."),
    ("Fatima S.", 5, "Great service and fast delivery to Sharjah. Packaged well."),
    ("Mohammed A.", 4, "Good product but came a day late. Still recommend."),
    ("Layla H.", 5, "Perfect condition, sealed box, best price in UAE."),
    ("Omar R.", 5, "Honest shop, good warranty, trustworthy."),
    ("Zara M.", 4, "Exactly what I expected. Price is fair."),
    ("Hassan T.", 5, "Tried Tamara, approval was instant. Very smooth checkout."),
    ("Aisha N.", 5, "Called for repair quote — they picked up within seconds."),
]


class Command(BaseCommand):
    help = "Seed all demo data: products, repair services, reviews, sample orders, demo user."

    def handle(self, *args, **options):
        self.stdout.write("Seeding catalog...")
        call_command("seed_demo")

        self.stdout.write("Seeding repair services...")
        for name, device, desc, price, minutes, icon, featured, order in REPAIR_SERVICES:
            RepairService.objects.update_or_create(
                name=name,
                defaults={
                    "device": device,
                    "short_desc": desc,
                    "description": desc + " Book online and drop off at our Rolla, Sharjah flagship.",
                    "base_price": Decimal(str(price)),
                    "est_minutes": minutes,
                    "icon": icon,
                    "is_featured": featured,
                    "order": order,
                },
            )

        self.stdout.write("Seeding reviews...")
        random.seed(42)
        for product in Product.objects.all():
            existing = product.reviews.count()
            target = random.randint(3, 6)
            for _ in range(max(0, target - existing)):
                user, rating, text = random.choice(REVIEWS)
                Review.objects.create(
                    product=product, user=user, rating=rating, text=text,
                )

        self.stdout.write("Creating demo user...")
        demo, created = User.objects.get_or_create(
            email="demo@shahzad.ae",
            defaults={"username": "demo@shahzad.ae", "first_name": "Demo", "last_name": "User"},
        )
        if created or not demo.has_usable_password():
            demo.set_password("Demo1234!")
            demo.save()
        Address.objects.get_or_create(
            user=demo, address_line1="Rolla Square, Al Wahda St",
            defaults={
                "name": "Demo User", "phone": "+971501234567",
                "city": "Sharjah", "postal_code": "00000", "country": "UAE", "is_default": True,
            },
        )

        admin, admin_created = User.objects.get_or_create(
            email="admin@shahzad.ae",
            defaults={
                "username": "admin@shahzad.ae", "first_name": "Admin", "last_name": "User",
                "is_staff": True, "is_superuser": True,
            },
        )
        if admin_created:
            admin.set_password("Admin1234!")
            admin.save()

        self.stdout.write("Seeding sample orders...")
        products = list(Product.objects.all()[:12])
        if products and Order.objects.filter(user=demo).count() < 3:
            for i in range(3):
                picks = random.sample(products, k=random.randint(1, 3))
                subtotal = sum((p.price for p in picks), Decimal("0"))
                order = Order.objects.create(
                    user=demo,
                    name="Demo User", email=demo.email, phone="+971501234567",
                    address_line1="Rolla Square, Al Wahda St", city="Sharjah",
                    postal_code="00000", country="UAE",
                    currency="AED", subtotal=subtotal, total=subtotal,
                    payment_method=random.choice(["cod", "tamara", "tabby"]),
                    provider=random.choice(["cod", "tamara", "tabby"]),
                    status=random.choice(["pending", "paid", "shipped", "delivered"]),
                    paid=random.choice([True, False]),
                )
                for p in picks:
                    OrderItem.objects.create(
                        order=order, product=p, title=p.title,
                        unit_price=p.price, quantity=1, image=p.primary_image,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Done.\n"
            f"  Products:        {Product.objects.count()}\n"
            f"  Reviews:         {Review.objects.count()}\n"
            f"  Repair services: {RepairService.objects.count()}\n"
            f"  Users:           {User.objects.count()}\n"
            f"  Orders:          {Order.objects.count()}\n"
            f"\nLogin credentials:\n"
            f"  Customer: demo@shahzad.ae  / Demo1234!\n"
            f"  Admin:    admin@shahzad.ae / Admin1234!  (/admin/)"
        ))
