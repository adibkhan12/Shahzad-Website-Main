from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.repairs.models import RepairService


SERVICES = [
    # (name, device, base_price, est_minutes, icon, short_desc, featured, order)
    ("iPhone Screen Replacement",  "phone",  "299.00",  45, "📱", "Genuine OEM display, lifetime warranty on labour.",  True,  10),
    ("Android Screen Replacement", "phone",  "249.00",  45, "📱", "All major brands — Samsung, Xiaomi, Pixel, Huawei.",   True,  20),
    ("Battery Replacement",        "phone",  "149.00",  30, "🔋", "Restore full-day battery life. Same-day service.",     True,  30),
    ("Charging Port Repair",       "phone",  "129.00",  60, "🔌", "Fix slow charging, no detection, loose ports.",       False, 40),
    ("Water Damage Diagnosis",     "phone",  "99.00",   60, "💧", "Free diagnosis, transparent quote before any work.",  False, 50),
    ("Speaker / Mic Repair",       "phone",  "139.00",  45, "🔊", "Get clear calls and audio back.",                     False, 60),
    ("Camera Module Replacement",  "phone",  "199.00",  60, "📸", "Front and rear camera modules.",                      False, 70),

    ("Laptop Screen Replacement",  "laptop", "599.00",  90, "💻", "FHD, 4K and OLED panels for all major brands.",       True,  100),
    ("Laptop Battery Replacement", "laptop", "349.00",  45, "🔋", "Genuine cells, 1-year warranty.",                     False, 110),
    ("Keyboard Replacement",       "laptop", "299.00",  60, "⌨️", "Sticky keys, dead keys, full keyboard swap.",         False, 120),
    ("Liquid Spill Cleaning",      "laptop", "249.00", 120, "💧", "Ultrasonic clean of motherboard, save your data.",    False, 130),
    ("SSD Upgrade & Migration",    "laptop", "399.00",  60, "💾", "Includes new NVMe SSD up to 1TB + Windows clone.",    False, 140),
    ("RAM Upgrade",                "laptop", "199.00",  30, "🧠", "Boost performance — DDR4 / DDR5 modules.",            False, 150),
    ("Software / Virus Cleanup",   "laptop", "149.00",  90, "🛡️", "Slow PC fix, virus removal, fresh Windows install.",  False, 160),

    ("Tablet Screen Replacement",  "tablet", "499.00",  90, "📲", "iPad, Galaxy Tab, and more.",                         False, 200),
    ("Watch Screen Replacement",   "watch",  "399.00",  90, "⌚", "Apple Watch, Galaxy Watch, Garmin.",                  False, 210),
]


class Command(BaseCommand):
    help = "Seed mobile/laptop/tablet repair services."

    def handle(self, *args, **opts):
        for name, device, price, mins, icon, short_desc, featured, order in SERVICES:
            RepairService.objects.update_or_create(
                name=name,
                defaults={
                    "device": device,
                    "base_price": Decimal(price),
                    "est_minutes": mins,
                    "icon": icon,
                    "short_desc": short_desc,
                    "is_featured": featured,
                    "order": order,
                    "description": (
                        f"{short_desc} Free diagnosis, no-fix-no-fee guarantee. "
                        "Walk-in or send-in service available."
                    ),
                },
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {RepairService.objects.count()} repair services."))
