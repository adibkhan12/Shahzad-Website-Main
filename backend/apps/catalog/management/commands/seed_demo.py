from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.catalog.models import AdBanner, Brand, Category, Product


# (title, brand, price, sale_price, category, image, featured)
# price = regular price (shown struck-through when on sale)
# sale_price = optional discounted price (what the customer actually pays)
DEMO = [
    ("iPhone 15 Pro Max 256GB", "Apple", "5799.00", "5299.00", "Smartphones",
     "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800", True),
    ("Samsung Galaxy S24 Ultra", "Samsung", "5199.00", "4799.00", "Smartphones",
     "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800", True),
    ("Google Pixel 8 Pro", "Google", "3699.00", None, "Smartphones",
     "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800", False),
    ("Xiaomi 14 Ultra", "Xiaomi", "3599.00", "3299.00", "Smartphones",
     "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=800", False),

    ("MacBook Pro 14\" M3 Pro", "Apple", "9499.00", "8999.00", "Laptops",
     "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800", True),
    ("Dell XPS 15 OLED", "Dell", "7299.00", None, "Laptops",
     "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800", False),
    ("Lenovo ThinkPad X1 Carbon", "Lenovo", "6999.00", "6499.00", "Laptops",
     "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800", False),
    ("ASUS ROG Zephyrus G14", "ASUS", "5999.00", None, "Laptops",
     "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800", False),

    ("iPad Pro 12.9\" M2", "Apple", "4899.00", "4499.00", "Tablets",
     "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=800", False),
    ("Samsung Tab S9 Ultra", "Samsung", "3999.00", None, "Tablets",
     "https://images.unsplash.com/photo-1542751110-97427bbecf20?w=800", False),

    ("AirPods Pro 2 (USB-C)", "Apple", "999.00", "899.00", "Audio",
     "https://images.unsplash.com/photo-1606220838315-056192d5e927?w=800", True),
    ("Sony WH-1000XM5", "Sony", "1599.00", "1399.00", "Audio",
     "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800", False),
    ("Bose QuietComfort Ultra", "Bose", "1599.00", None, "Audio",
     "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800", False),

    ("Anker 65W GaN Charger", "Anker", "229.00", "189.00", "Chargers & Cables",
     "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800", False),
    ("Apple 20W USB-C Adapter", "Apple", "89.00", None, "Chargers & Cables",
     "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800", False),
    ("USB-C to Lightning Cable 1m", "Apple", "99.00", "79.00", "Chargers & Cables",
     "https://images.unsplash.com/photo-1625948514430-3a3f56cd1e9c?w=800", False),

    ("iPhone 15 Pro Silicone Case", "Apple", "189.00", None, "Cases & Covers",
     "https://images.unsplash.com/photo-1551355738-b4e30af40d92?w=800", False),
    ("MacBook Pro 14 Sleeve", "tomtoc", "159.00", "129.00", "Cases & Covers",
     "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800", False),

    ("Samsung T7 Shield 1TB SSD", "Samsung", "529.00", "449.00", "Storage",
     "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800", False),
    ("SanDisk Extreme microSD 256GB", "SanDisk", "159.00", None, "Storage",
     "https://images.unsplash.com/photo-1608085575257-95dabd0ad4ee?w=800", False),

    ("Apple Watch Series 9 GPS", "Apple", "1699.00", "1499.00", "Wearables",
     "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800", False),
    ("Samsung Galaxy Watch 6", "Samsung", "999.00", None, "Wearables",
     "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800", False),
]

BANNERS = [
    ("New iPhone 15 Pro", "In stock — same-day delivery across Sharjah", "Shop iPhone", "/products?category=smartphones", "#740DC2", 0),
    ("Cracked screen?", "Phone & laptop repairs in 30 minutes", "Book a repair", "/repairs", "#DC2626", 1),
    ("MacBook bundles", "Save up to AED 800 on M3 laptops", "Shop laptops", "/products?category=laptops", "#0EA5E9", 2),
]


class Command(BaseCommand):
    help = "Seed mobile/laptop/accessories catalog + brands + banners."

    def handle(self, *args, **options):
        cats = {}
        for name in sorted({row[4] for row in DEMO}):
            cat, _ = Category.objects.get_or_create(name=name)
            cats[name] = cat

        # Brands are scoped per category (Apple for Smartphones is a different brand row
        # than Apple for Laptops — this is what you asked for in the hierarchy).
        brands = {}
        for _, brand_name, _, _, cat_name, _, _ in DEMO:
            key = (brand_name, cats[cat_name].id)
            if key not in brands:
                b, _created = Brand.objects.get_or_create(
                    name=brand_name, category=cats[cat_name],
                )
                brands[key] = b

        for title, brand_name, price, sale, cat_name, image, featured in DEMO:
            Product.objects.update_or_create(
                title=title,
                defaults={
                    "brand": brands[(brand_name, cats[cat_name].id)],
                    "price": Decimal(price),
                    "sale_price": Decimal(sale) if sale else None,
                    "category": cats[cat_name],
                    "images": [image],
                    "stock": 15,
                    "is_active": True,
                    "is_featured": featured,
                    "description": (
                        f"{title} — genuine {brand_name}, sealed retail box, 1-year manufacturer warranty. "
                        f"Free same-day delivery across Sharjah, next-day across the UAE. Trade-in accepted."
                    ),
                },
            )

        AdBanner.objects.all().delete()
        for title, desc, button, link, bg, order in BANNERS:
            AdBanner.objects.create(
                title=title, desc=desc, button=button, link=link, bg=bg, order=order,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Product.objects.count()} products, {Brand.objects.count()} brands "
            f"across {Category.objects.count()} categories, {AdBanner.objects.count()} banners."
        ))
