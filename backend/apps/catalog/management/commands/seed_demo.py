"""
Seed a realistic Shahzad Mobile catalog: smartphones, tablets, laptops,
audio, wearables, and accessories with brand-accurate names, descriptions,
AED pricing, varied stock levels, and a mix of on-sale items.

Idempotent: safe to re-run; updates existing products by title.
"""

from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.catalog.models import AdBanner, Brand, Category, Product

# Description footer reused per category to keep tone consistent.
WARRANTY_PHONE = (
    "Sealed retail box, 1-year UAE warranty. Free same-day delivery in Sharjah, next-day UAE-wide."
)
WARRANTY_LAPTOP = (
    "Sealed retail box, 1-year manufacturer warranty. Free delivery and basic setup on request."
)
WARRANTY_AUDIO = "Sealed retail box, 1-year manufacturer warranty. Free delivery across the UAE."
WARRANTY_WEAR = (
    "Sealed retail box, 1-year manufacturer warranty. Free delivery and band-fit help in store."
)
WARRANTY_GENERIC = "1-year warranty. Free delivery on orders over AED 100."

PRODUCTS = [
    # --- Smartphones ---
    {
        "title": "iPhone 15 Pro Max 256GB Natural Titanium",
        "brand": "Apple",
        "category": "Smartphones",
        "price": "4699.00",
        "sale_price": None,
        "stock": 12,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800",
        "description": (
            "6.7-inch Super Retina XDR OLED with ProMotion. A17 Pro chip, 48MP "
            "main + 5x telephoto. Titanium frame, USB-C, Action button. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "iPhone 15 Pro 128GB Blue Titanium",
        "brand": "Apple",
        "category": "Smartphones",
        "price": "4099.00",
        "sale_price": None,
        "stock": 18,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800",
        "description": (
            "6.1-inch Super Retina XDR OLED, A17 Pro, 48MP main camera, 3x telephoto. "
            "USB-C, Action button, titanium build. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "iPhone 15 128GB Pink",
        "brand": "Apple",
        "category": "Smartphones",
        "price": "3299.00",
        "sale_price": "3099.00",
        "stock": 25,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1631016800696-5ea8801b3c2a?w=800",
        "description": (
            "6.1-inch Super Retina XDR, A16 Bionic, 48MP main camera. Dynamic Island, "
            "USB-C. Includes USB-C charge cable. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "iPhone 14 128GB Midnight",
        "brand": "Apple",
        "category": "Smartphones",
        "price": "2799.00",
        "sale_price": "2599.00",
        "stock": 15,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1663499482523-1c0c1bae4ce1?w=800",
        "description": (
            "6.1-inch OLED, A15 Bionic, dual 12MP camera, all-day battery. "
            "5G, MagSafe. Excellent value flagship. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Samsung Galaxy S24 Ultra 256GB Titanium Gray",
        "brand": "Samsung",
        "category": "Smartphones",
        "price": "4799.00",
        "sale_price": "4499.00",
        "stock": 8,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800",
        "description": (
            "6.8-inch Dynamic AMOLED 2X 120Hz, Snapdragon 8 Gen 3 for Galaxy. "
            "200MP main + 50MP 5x periscope. Built-in S Pen, titanium frame. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Samsung Galaxy S24+ 256GB Onyx Black",
        "brand": "Samsung",
        "category": "Smartphones",
        "price": "3699.00",
        "sale_price": None,
        "stock": 22,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800",
        "description": (
            "6.7-inch Dynamic AMOLED 2X QHD+, Snapdragon 8 Gen 3, 12GB RAM. "
            "50MP triple camera with 3x optical zoom. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Samsung Galaxy A55 5G 128GB Awesome Iceblue",
        "brand": "Samsung",
        "category": "Smartphones",
        "price": "1499.00",
        "sale_price": "1299.00",
        "stock": 50,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800",
        "description": (
            "6.6-inch Super AMOLED 120Hz, Exynos 1480, 50MP OIS main camera, 5000mAh "
            "battery. IP67 water resistance. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Google Pixel 8 Pro 128GB Bay",
        "brand": "Google",
        "category": "Smartphones",
        "price": "3699.00",
        "sale_price": None,
        "stock": 6,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800",
        "description": (
            "6.7-inch Super Actua LTPO 120Hz, Tensor G3 chip. Pro triple camera with "
            "5x telephoto, Magic Eraser, Best Take. 7 years of OS updates. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Xiaomi 14 Ultra 512GB Black",
        "brand": "Xiaomi",
        "category": "Smartphones",
        "price": "3299.00",
        "sale_price": "2999.00",
        "stock": 9,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1567581935884-3349723552ca?w=800",
        "description": (
            "Leica quad camera with 1-inch sensor, Snapdragon 8 Gen 3, 6.73-inch LTPO "
            "AMOLED. 90W wired charging. Photography flagship. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "OnePlus 12 256GB Silky Black",
        "brand": "OnePlus",
        "category": "Smartphones",
        "price": "2899.00",
        "sale_price": None,
        "stock": 14,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1546054454-aa26e2b734c7?w=800",
        "description": (
            "6.82-inch ProXDR LTPO 4.0, Snapdragon 8 Gen 3, 16GB RAM. Hasselblad triple "
            "camera. 100W SUPERVOOC + 50W AIRVOOC wireless. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Nothing Phone (2a) 256GB Milk",
        "brand": "Nothing",
        "category": "Smartphones",
        "price": "1399.00",
        "sale_price": "1199.00",
        "stock": 30,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800",
        "description": (
            "6.7-inch flexible AMOLED 120Hz, Dimensity 7200 Pro. Iconic Glyph LED "
            "interface on the back. Clean Nothing OS 2.5. " + WARRANTY_PHONE
        ),
    },
    {
        "title": "Honor Magic 6 Pro 512GB Epi Green",
        "brand": "Honor",
        "category": "Smartphones",
        "price": "2999.00",
        "sale_price": None,
        "stock": 0,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800",
        "description": (
            "6.8-inch LTPO AMOLED 120Hz, Snapdragon 8 Gen 3. 180MP periscope telephoto, "
            "AI-powered Magic Capsule. 5600mAh battery. " + WARRANTY_PHONE
        ),
    },
    # --- Tablets ---
    {
        "title": 'iPad Pro 12.9" M2 256GB Wi-Fi Space Gray',
        "brand": "Apple",
        "category": "Tablets",
        "price": "4499.00",
        "sale_price": "4199.00",
        "stock": 10,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=800",
        "description": (
            "12.9-inch Liquid Retina XDR mini-LED, M2 chip, 8GB RAM. ProMotion 120Hz, "
            "Apple Pencil hover. Thunderbolt USB-C. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": 'iPad Pro 11" M4 256GB Wi-Fi Silver',
        "brand": "Apple",
        "category": "Tablets",
        "price": "3899.00",
        "sale_price": None,
        "stock": 14,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=800",
        "description": (
            "11-inch Ultra Retina XDR tandem OLED, M4 chip, 8GB RAM. Thinner design, "
            "Apple Pencil Pro support. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": 'iPad Air 11" M2 128GB Wi-Fi Blue',
        "brand": "Apple",
        "category": "Tablets",
        "price": "2499.00",
        "sale_price": "2299.00",
        "stock": 20,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=800",
        "description": (
            "11-inch Liquid Retina, M2 chip, 8GB RAM. Apple Pencil Pro & USB-C Magic "
            "Keyboard support. Lighter than Pro. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": "iPad 10th Gen 64GB Wi-Fi Silver",
        "brand": "Apple",
        "category": "Tablets",
        "price": "1499.00",
        "sale_price": None,
        "stock": 35,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800",
        "description": (
            "10.9-inch Liquid Retina, A14 Bionic, USB-C, landscape FaceTime camera. "
            "Best-value iPad for everyday use. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": "Samsung Galaxy Tab S9 Ultra 256GB Wi-Fi Graphite",
        "brand": "Samsung",
        "category": "Tablets",
        "price": "3999.00",
        "sale_price": None,
        "stock": 7,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1542751110-97427bbecf20?w=800",
        "description": (
            "14.6-inch Dynamic AMOLED 2X 120Hz, Snapdragon 8 Gen 2 for Galaxy. "
            "Includes S Pen. IP68 water resistance. " + WARRANTY_LAPTOP
        ),
    },
    # --- Laptops ---
    {
        "title": 'MacBook Pro 14" M3 Pro 18GB / 512GB Space Black',
        "brand": "Apple",
        "category": "Laptops",
        "price": "8999.00",
        "sale_price": "8499.00",
        "stock": 5,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800",
        "description": (
            "14-inch Liquid Retina XDR mini-LED 120Hz. M3 Pro: 11-core CPU, 14-core GPU. "
            "Up to 18 hours battery. Includes 70W USB-C adapter. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": 'MacBook Air 13" M3 16GB / 256GB Midnight',
        "brand": "Apple",
        "category": "Laptops",
        "price": "4999.00",
        "sale_price": None,
        "stock": 12,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800",
        "description": (
            "13.6-inch Liquid Retina, M3 chip 8-core CPU, 10-core GPU. Up to 18 hours "
            "battery. Fanless silent design. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": 'MacBook Air 15" M2 8GB / 256GB Starlight',
        "brand": "Apple",
        "category": "Laptops",
        "price": "4699.00",
        "sale_price": "4399.00",
        "stock": 8,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800",
        "description": (
            "15.3-inch Liquid Retina, M2 chip. Six-speaker sound system, MagSafe "
            "charging. Largest-screen Air. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": "Dell XPS 15 OLED Core i7 / 32GB / 1TB",
        "brand": "Dell",
        "category": "Laptops",
        "price": "7299.00",
        "sale_price": None,
        "stock": 4,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800",
        "description": (
            "15.6-inch 3.5K OLED InfinityEdge touchscreen. Intel Core i7-13700H, "
            "RTX 4060, 32GB DDR5, 1TB NVMe. CNC machined aluminum. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": "Lenovo ThinkPad X1 Carbon Gen 12 Core i7 / 16GB / 1TB",
        "brand": "Lenovo",
        "category": "Laptops",
        "price": "6499.00",
        "sale_price": "5999.00",
        "stock": 6,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800",
        "description": (
            "14-inch 2.8K OLED, Intel Core Ultra 7. 16GB LPDDR5X, 1TB SSD. "
            "MIL-SPEC durability, ThinkShutter privacy. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": "ASUS ROG Zephyrus G14 Ryzen 9 / RTX 4060 / 1TB",
        "brand": "ASUS",
        "category": "Laptops",
        "price": "5999.00",
        "sale_price": None,
        "stock": 3,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800",
        "description": (
            "14-inch QHD+ OLED 120Hz Nebula display. Ryzen 9 8945HS, RTX 4060, 16GB "
            "DDR5, 1TB NVMe. AniMe Matrix LED lid. " + WARRANTY_LAPTOP
        ),
    },
    {
        "title": "HP Spectre x360 14 Core Ultra 7 / 16GB / 1TB",
        "brand": "HP",
        "category": "Laptops",
        "price": "5499.00",
        "sale_price": None,
        "stock": 5,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800",
        "description": (
            "14-inch 2.8K OLED touch convertible. Core Ultra 7 155H, 16GB LPDDR5x, 1TB. "
            "Includes HP MPP2.0 tilt pen. " + WARRANTY_LAPTOP
        ),
    },
    # --- Audio ---
    {
        "title": "AirPods Pro 2 (USB-C)",
        "brand": "Apple",
        "category": "Audio",
        "price": "899.00",
        "sale_price": "799.00",
        "stock": 40,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1606220838315-056192d5e927?w=800",
        "description": (
            "Adaptive Audio, Active Noise Cancellation, Conversation Awareness. "
            "Up to 30 hours with charging case. USB-C MagSafe case. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "AirPods Max Space Gray",
        "brand": "Apple",
        "category": "Audio",
        "price": "2299.00",
        "sale_price": None,
        "stock": 8,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800",
        "description": (
            "Over-ear, computational audio, Spatial Audio with dynamic head tracking. "
            "20-hour battery. Premium aluminum + memory foam. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "AirPods 4 with Active Noise Cancellation",
        "brand": "Apple",
        "category": "Audio",
        "price": "799.00",
        "sale_price": None,
        "stock": 25,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800",
        "description": (
            "Open-ear design with H2 chip ANC. Personalized Spatial Audio, Voice "
            "Isolation. Wireless charging case. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "Sony WH-1000XM5 Black",
        "brand": "Sony",
        "category": "Audio",
        "price": "1399.00",
        "sale_price": "1199.00",
        "stock": 12,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800",
        "description": (
            "Industry-leading noise cancellation, 8 microphones. 30-hour battery, "
            "LDAC + DSEE Extreme. Multipoint Bluetooth. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "Sony WF-1000XM5",
        "brand": "Sony",
        "category": "Audio",
        "price": "1199.00",
        "sale_price": None,
        "stock": 18,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800",
        "description": (
            "Smallest, lightest XM-series in-ears. Integrated processor V2 + V1. "
            "8-hour battery (24 with case). Crystal-clear calls. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "Bose QuietComfort Ultra Headphones",
        "brand": "Bose",
        "category": "Audio",
        "price": "1599.00",
        "sale_price": None,
        "stock": 6,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=800",
        "description": (
            "Immersive Audio with Spatial-aware playback. World-class noise cancellation. "
            "24-hour battery, plush memory foam earcups. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "Samsung Galaxy Buds 2 Pro",
        "brand": "Samsung",
        "category": "Audio",
        "price": "799.00",
        "sale_price": "649.00",
        "stock": 22,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1606220838315-056192d5e927?w=800",
        "description": (
            "Hi-Fi 24-bit audio, intelligent ANC, 360 Audio. IPX7 water resistance. "
            "Seamless switching across Galaxy devices. " + WARRANTY_AUDIO
        ),
    },
    {
        "title": "JBL Charge 5 Bluetooth Speaker Black",
        "brand": "JBL",
        "category": "Audio",
        "price": "599.00",
        "sale_price": "499.00",
        "stock": 30,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800",
        "description": (
            "20-hour playtime, IP67 dust/water proof. Built-in powerbank to charge "
            "your phone. PartyBoost to pair multiple JBLs. " + WARRANTY_AUDIO
        ),
    },
    # --- Wearables ---
    {
        "title": "Apple Watch Ultra 2 49mm Titanium Trail Loop",
        "brand": "Apple",
        "category": "Wearables",
        "price": "3299.00",
        "sale_price": None,
        "stock": 6,
        "featured": True,
        "image": "https://images.unsplash.com/photo-1551816230-ef5deaed4a26?w=800",
        "description": (
            "Brightest-ever Apple Watch display, S9 chip. Action button, Dive computer, "
            "GPS precision dual-frequency. Up to 36-hour battery. " + WARRANTY_WEAR
        ),
    },
    {
        "title": "Apple Watch Series 9 GPS 41mm Midnight",
        "brand": "Apple",
        "category": "Wearables",
        "price": "1499.00",
        "sale_price": "1299.00",
        "stock": 18,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800",
        "description": (
            "S9 chip, Double Tap gesture, brighter display. ECG, Blood Oxygen, "
            "temperature sensing. " + WARRANTY_WEAR
        ),
    },
    {
        "title": "Apple Watch SE 2nd Gen 40mm Starlight",
        "brand": "Apple",
        "category": "Wearables",
        "price": "999.00",
        "sale_price": None,
        "stock": 30,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800",
        "description": (
            "S8 chip, all the essentials at a friendlier price. Crash and Fall "
            "detection, fitness tracking, family setup. " + WARRANTY_WEAR
        ),
    },
    {
        "title": "Samsung Galaxy Watch 6 Classic 47mm",
        "brand": "Samsung",
        "category": "Wearables",
        "price": "1399.00",
        "sale_price": None,
        "stock": 10,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800",
        "description": (
            "Rotating bezel returns. Sleep Insights, advanced workout tracking, body "
            "composition analysis. Wear OS 4. " + WARRANTY_WEAR
        ),
    },
    {
        "title": "Garmin Fenix 7 Sapphire Solar Titanium",
        "brand": "Garmin",
        "category": "Wearables",
        "price": "3899.00",
        "sale_price": None,
        "stock": 4,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1617043786394-f977fa12eddf?w=800",
        "description": (
            "Solar-charging multisport GPS. Built for the toughest adventures. "
            "Up to 22 days battery, multi-band GNSS. " + WARRANTY_WEAR
        ),
    },
    # --- Chargers & Cables ---
    {
        "title": "Anker 65W GaN II 3-Port Charger",
        "brand": "Anker",
        "category": "Chargers & Cables",
        "price": "189.00",
        "sale_price": "159.00",
        "stock": 60,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800",
        "description": (
            "65W total across two USB-C and one USB-A. Fast-charge MacBook Air, iPad "
            "Pro, iPhone simultaneously. Foldable plug. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": "Apple 20W USB-C Power Adapter",
        "brand": "Apple",
        "category": "Chargers & Cables",
        "price": "89.00",
        "sale_price": None,
        "stock": 100,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=800",
        "description": (
            "Fast-charges iPhone 8 and later up to 50% in 30 minutes. Compact, single "
            "USB-C port. Cable sold separately. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": "Apple MagSafe Charger 1m",
        "brand": "Apple",
        "category": "Chargers & Cables",
        "price": "159.00",
        "sale_price": None,
        "stock": 45,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=800",
        "description": (
            "Up to 15W wireless charging for iPhone 12 and later. Magnetic alignment, "
            "USB-C connector. Power adapter not included. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": "Belkin BoostCharge Pro 3-in-1 MagSafe Wireless Stand",
        "brand": "Belkin",
        "category": "Chargers & Cables",
        "price": "599.00",
        "sale_price": None,
        "stock": 12,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1593642533144-3d62aa4783ec?w=800",
        "description": (
            "Charges iPhone 15W MagSafe, Apple Watch fast-charge, AirPods at the same "
            "time. Premium aluminum stand. " + WARRANTY_GENERIC
        ),
    },
    # --- Cases & Covers ---
    {
        "title": "iPhone 15 Pro Silicone Case with MagSafe — Cypress",
        "brand": "Apple",
        "category": "Cases & Covers",
        "price": "189.00",
        "sale_price": None,
        "stock": 35,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1601972602288-3be527b4f18a?w=800",
        "description": (
            "Apple silicone with soft microfibre lining. Built-in magnets align with "
            "MagSafe accessories. Slim, grippy. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": "Samsung Galaxy S24 Ultra Smart View Wallet Case",
        "brand": "Samsung",
        "category": "Cases & Covers",
        "price": "179.00",
        "sale_price": None,
        "stock": 25,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1601972602288-3be527b4f18a?w=800",
        "description": (
            "View notifications and answer calls without opening. Card slot, "
            "kickstand. Genuine Samsung accessory. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": 'Spigen Tough Armor MacBook Pro 14" Sleeve',
        "brand": "Spigen",
        "category": "Cases & Covers",
        "price": "159.00",
        "sale_price": "129.00",
        "stock": 20,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800",
        "description": (
            "Microfibre interior, water-resistant exterior, magnetic flap closure. "
            "Front pocket for charger and dongles. " + WARRANTY_GENERIC
        ),
    },
    # --- Storage ---
    {
        "title": "Samsung T7 Shield 1TB Portable SSD Black",
        "brand": "Samsung",
        "category": "Storage",
        "price": "449.00",
        "sale_price": "399.00",
        "stock": 28,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800",
        "description": (
            "Up to 1,050 MB/s read, 1,000 MB/s write. IP65 dust/water resistant, "
            "drop-tested to 3m. USB 3.2 Gen 2 USB-C. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": "SanDisk Extreme microSDXC 256GB",
        "brand": "SanDisk",
        "category": "Storage",
        "price": "159.00",
        "sale_price": None,
        "stock": 80,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=800",
        "description": (
            "Up to 190MB/s read, 130MB/s write. A2, V30, U3 — perfect for 4K UHD "
            "video and Nintendo Switch. Includes SD adapter. " + WARRANTY_GENERIC
        ),
    },
    {
        "title": "WD My Passport 4TB External Hard Drive",
        "brand": "WD",
        "category": "Storage",
        "price": "399.00",
        "sale_price": None,
        "stock": 18,
        "featured": False,
        "image": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800",
        "description": (
            "USB 3.2 Gen 1, 256-bit AES hardware encryption. Auto backup with WD "
            "Backup software. Plug-and-play on Windows; reformat for macOS. " + WARRANTY_GENERIC
        ),
    },
]

BANNERS = [
    {
        "title": "iPhone 15 Pro Max",
        "desc": "In stock — same-day delivery across Sharjah",
        "button": "Shop iPhone",
        "link": "/products?category=smartphones",
        "bg": "#740DC2",
    },
    {
        "title": "Cracked screen?",
        "desc": "Phone & laptop repairs in 30 minutes",
        "button": "Book a repair",
        "link": "/repairs",
        "bg": "#DC2626",
    },
    {
        "title": "MacBook bundles",
        "desc": "Save up to AED 800 on M3 laptops",
        "button": "Shop laptops",
        "link": "/products?category=laptops",
        "bg": "#0EA5E9",
    },
    {
        "title": "Galaxy S24 Ultra",
        "desc": "Free Galaxy Buds 2 Pro with every Ultra",
        "button": "Shop Samsung",
        "link": "/products?brand=samsung",
        "bg": "#1E293B",
    },
    {
        "title": "Pay with Tamara or Tabby",
        "desc": "Split into 4 — interest-free",
        "button": "Learn how",
        "link": "/payment-options",
        "bg": "#059669",
    },
]


class Command(BaseCommand):
    help = "Seed a realistic catalog: ~45 products, brands, categories, banners."

    def handle(self, *args, **options):
        # Categories
        cats = {}
        for name in sorted({p["category"] for p in PRODUCTS}):
            cat, _ = Category.objects.get_or_create(name=name)
            cats[name] = cat

        # Brands are scoped per category (Apple in Smartphones != Apple in Laptops).
        brands = {}
        for p in PRODUCTS:
            cat = cats[p["category"]]
            key = (p["brand"], cat.id)
            if key not in brands:
                brand, _ = Brand.objects.get_or_create(name=p["brand"], category=cat)
                brands[key] = brand

        # Products
        for p in PRODUCTS:
            cat = cats[p["category"]]
            brand = brands[(p["brand"], cat.id)]
            Product.objects.update_or_create(
                title=p["title"],
                defaults={
                    "brand": brand,
                    "category": cat,
                    "price": Decimal(p["price"]),
                    "sale_price": Decimal(p["sale_price"]) if p["sale_price"] else None,
                    "stock": p["stock"],
                    "is_active": True,
                    "is_featured": p["featured"],
                    "images": [p["image"]],
                    "description": p["description"],
                },
            )

        # Banners — wipe + recreate to honour the order in the list
        AdBanner.objects.all().delete()
        for i, b in enumerate(BANNERS):
            AdBanner.objects.create(
                title=b["title"],
                desc=b["desc"],
                button=b["button"],
                link=b["link"],
                bg=b["bg"],
                order=i,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {Product.objects.count()} products across "
                f"{Category.objects.count()} categories, {Brand.objects.count()} brand "
                f"entries, {AdBanner.objects.count()} banners."
            )
        )
