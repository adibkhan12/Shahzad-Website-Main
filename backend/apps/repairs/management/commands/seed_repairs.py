"""
Seed Shahzad Mobile's repair services catalog: phone, laptop, tablet, watch.
Idempotent — safe to re-run; updates by service name.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.repairs.models import RepairService

GUARANTEE = (
    "Free walk-in diagnosis with no-fix-no-fee guarantee. Most jobs done same-day "
    "at our Rolla, Sharjah store. Genuine OEM-grade parts; we never use cheap copies."
)

SERVICES = [
    # --- Phone ---
    {
        "name": "iPhone Screen Replacement",
        "device": "phone",
        "price": "299.00",
        "minutes": 45,
        "icon": "📱",
        "featured": True,
        "order": 10,
        "short_desc": "Genuine OLED display, lifetime labour warranty.",
        "description": (
            "Apple-grade OLED panels for iPhone 8 through iPhone 15 Pro Max. Includes "
            "True Tone calibration, Face ID re-verification, and a lifetime labour "
            "warranty. " + GUARANTEE
        ),
    },
    {
        "name": "Android Screen Replacement",
        "device": "phone",
        "price": "249.00",
        "minutes": 45,
        "icon": "📱",
        "featured": True,
        "order": 20,
        "short_desc": "Samsung, Xiaomi, Pixel, OnePlus, Huawei, Honor.",
        "description": (
            "Original Service Pack and OEM-grade replacement panels. AMOLED, OLED and "
            "LCD all supported. Full digitiser test before handover. " + GUARANTEE
        ),
    },
    {
        "name": "Phone Battery Replacement",
        "device": "phone",
        "price": "149.00",
        "minutes": 30,
        "icon": "🔋",
        "featured": True,
        "order": 30,
        "short_desc": "Restore full-day battery life. Same-day service.",
        "description": (
            "We use only fresh-cell, 0-cycle batteries — never refurbished. Includes "
            "battery health calibration and a 6-month warranty. " + GUARANTEE
        ),
    },
    {
        "name": "Charging Port Repair",
        "device": "phone",
        "price": "129.00",
        "minutes": 60,
        "icon": "🔌",
        "featured": False,
        "order": 40,
        "short_desc": "Fix slow charging, no detection, loose ports.",
        "description": (
            "Lightning, USB-C and microUSB. Replacement of the entire charge-flex "
            "assembly when needed; ultrasonic clean if the port is just dirty. " + GUARANTEE
        ),
    },
    {
        "name": "Water Damage Diagnosis",
        "device": "phone",
        "price": "99.00",
        "minutes": 60,
        "icon": "💧",
        "featured": False,
        "order": 50,
        "short_desc": "Free transparent quote before any work.",
        "description": (
            "Ultrasonic motherboard cleaning, board-level component inspection, and "
            "data-recovery first. We give you a no-obligation quote before any repair. " + GUARANTEE
        ),
    },
    {
        "name": "Speaker / Microphone Repair",
        "device": "phone",
        "price": "139.00",
        "minutes": 45,
        "icon": "🔊",
        "featured": False,
        "order": 60,
        "short_desc": "Get clear calls and audio back.",
        "description": (
            "Earpiece, loudspeaker and microphone replacements. Often a quick fix "
            "after liquid exposure or accidental drops. " + GUARANTEE
        ),
    },
    {
        "name": "Camera Module Replacement",
        "device": "phone",
        "price": "199.00",
        "minutes": 60,
        "icon": "📸",
        "featured": False,
        "order": 70,
        "short_desc": "Front and rear camera modules.",
        "description": (
            "Cracked lens, blurry camera, no-detect issues. Front (selfie) or rear "
            "module replacement with full optical-image-stabilisation calibration. " + GUARANTEE
        ),
    },
    {
        "name": "Back Glass Replacement",
        "device": "phone",
        "price": "229.00",
        "minutes": 90,
        "icon": "🔁",
        "featured": False,
        "order": 80,
        "short_desc": "Restore the back glass on iPhone & Samsung.",
        "description": (
            "Laser-removed broken glass, then OEM-grade replacement back panel "
            "professionally adhesived. Wireless charging tested before return. " + GUARANTEE
        ),
    },
    # --- Laptop ---
    {
        "name": "Laptop Screen Replacement",
        "device": "laptop",
        "price": "599.00",
        "minutes": 90,
        "icon": "💻",
        "featured": True,
        "order": 100,
        "short_desc": "FHD, 4K and OLED panels for all major brands.",
        "description": (
            "Apple, Dell, HP, Lenovo, ASUS, MSI. Touch and non-touch displays. We "
            "match your original panel resolution and refresh rate exactly. " + GUARANTEE
        ),
    },
    {
        "name": "Laptop Battery Replacement",
        "device": "laptop",
        "price": "349.00",
        "minutes": 45,
        "icon": "🔋",
        "featured": False,
        "order": 110,
        "short_desc": "Genuine cells, 1-year warranty.",
        "description": (
            "All major brands, including MacBook (Apple service-pack batteries) and "
            "ThinkPads. Includes battery calibration after install. " + GUARANTEE
        ),
    },
    {
        "name": "Keyboard Replacement",
        "device": "laptop",
        "price": "299.00",
        "minutes": 60,
        "icon": "⌨️",
        "featured": False,
        "order": 120,
        "short_desc": "Sticky keys, dead keys, full keyboard swap.",
        "description": (
            "Per-key replacement when possible, full keyboard assembly when not. "
            "Includes backlight ribbon if your model supports it. " + GUARANTEE
        ),
    },
    {
        "name": "Liquid Spill Recovery",
        "device": "laptop",
        "price": "249.00",
        "minutes": 120,
        "icon": "💧",
        "featured": False,
        "order": 130,
        "short_desc": "Ultrasonic motherboard cleaning, save your data.",
        "description": (
            "Coffee, juice, or water — we strip down and ultrasonically clean every "
            "board. We always recover your data first when possible. " + GUARANTEE
        ),
    },
    {
        "name": "SSD Upgrade & Data Migration",
        "device": "laptop",
        "price": "399.00",
        "minutes": 60,
        "icon": "💾",
        "featured": False,
        "order": 140,
        "short_desc": "New NVMe SSD up to 2TB + Windows clone.",
        "description": (
            "Brand-name NVMe (Samsung, WD, Kingston). Includes full bit-by-bit clone "
            "of your old drive — boot back into your familiar setup. " + GUARANTEE
        ),
    },
    {
        "name": "RAM Upgrade",
        "device": "laptop",
        "price": "199.00",
        "minutes": 30,
        "icon": "🧠",
        "featured": False,
        "order": 150,
        "short_desc": "Boost performance — DDR4 / DDR5 modules.",
        "description": (
            "We check compatibility, supply Crucial / Kingston / Samsung modules and "
            "stress-test the install. Soldered laptops can only upgrade if there's a "
            "spare slot — we'll tell you straight. " + GUARANTEE
        ),
    },
    {
        "name": "Software / Virus Cleanup",
        "device": "laptop",
        "price": "149.00",
        "minutes": 90,
        "icon": "🛡️",
        "featured": False,
        "order": 160,
        "short_desc": "Slow PC fix, virus removal, fresh Windows.",
        "description": (
            "Full malware scan, junk-file purge, startup tuning. Fresh Windows install "
            "available — your files preserved. " + GUARANTEE
        ),
    },
    # --- Tablet ---
    {
        "name": "Tablet Screen Replacement",
        "device": "tablet",
        "price": "499.00",
        "minutes": 90,
        "icon": "📲",
        "featured": False,
        "order": 200,
        "short_desc": "iPad, Galaxy Tab, and more.",
        "description": (
            "Outer glass, full-display assembly, or digitiser-only — whichever your "
            "tablet needs. iPad Pro tandem-OLED replacements supported. " + GUARANTEE
        ),
    },
    {
        "name": "Tablet Battery Replacement",
        "device": "tablet",
        "price": "299.00",
        "minutes": 90,
        "icon": "🔋",
        "featured": False,
        "order": 210,
        "short_desc": "Restore battery life on iPad and Galaxy Tab.",
        "description": (
            "All-day battery returned. Includes battery-health calibration and a "
            "1-year warranty on parts. " + GUARANTEE
        ),
    },
    # --- Watch ---
    {
        "name": "Smart Watch Screen Replacement",
        "device": "watch",
        "price": "399.00",
        "minutes": 90,
        "icon": "⌚",
        "featured": False,
        "order": 300,
        "short_desc": "Apple Watch, Galaxy Watch, Garmin.",
        "description": (
            "Crystal, OLED display assembly, and digitiser replacements. Includes "
            "water-resistance reseal where the original gasket allows. " + GUARANTEE
        ),
    },
    {
        "name": "Smart Watch Battery Replacement",
        "device": "watch",
        "price": "249.00",
        "minutes": 60,
        "icon": "🔋",
        "featured": False,
        "order": 310,
        "short_desc": "Apple Watch and Galaxy Watch battery refresh.",
        "description": (
            "Genuine-cell replacement, full battery health restored. Includes "
            "OS calibration and water-resistance reseal. " + GUARANTEE
        ),
    },
    # --- Other ---
    {
        "name": "Data Recovery",
        "device": "other",
        "price": "299.00",
        "minutes": 240,
        "icon": "🛟",
        "featured": False,
        "order": 400,
        "short_desc": "Recover photos, contacts, files from dead devices.",
        "description": (
            "Phones, tablets, laptops, USB drives, microSD. Logical recovery (formatted / "
            "deleted) and physical recovery (broken board, dead drive). Quote varies by "
            "severity — we always tell you upfront. " + GUARANTEE
        ),
    },
]


class Command(BaseCommand):
    help = "Seed mobile / laptop / tablet / watch repair services."

    def handle(self, *args, **opts):
        # Look up by slug (unique field) so we cleanly update existing rows even
        # when an old seed used a slightly different casing for the name.
        for s in SERVICES:
            slug = slugify(s["name"])[:160]
            RepairService.objects.update_or_create(
                slug=slug,
                defaults={
                    "name": s["name"],
                    "device": s["device"],
                    "base_price": Decimal(s["price"]),
                    "est_minutes": s["minutes"],
                    "icon": s["icon"],
                    "is_featured": s["featured"],
                    "order": s["order"],
                    "short_desc": s["short_desc"],
                    "description": s["description"],
                },
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {RepairService.objects.count()} repair services "
                f"({RepairService.objects.filter(is_featured=True).count()} featured)."
            )
        )
