from django.conf import settings

from apps.cart.services import get_or_create_cart
from apps.wishlist.models import WishedProduct

BRAND = {
    "name": "Shahzad Arshad",
    "legal_name": "Shahzad Arshad Elect. Devices tr",
    "short_name": "Shahzadmobile",
    "tagline": "Genuine gear. Same-day repairs.",
    "color": "#ff9900",
    "address_line1": "Rolla Mall, Second Floor, Shop 216",
    "address_line2": "Al Rolla, Sharjah",
    "country": "United Arab Emirates",
    "email": "sa@shahzadmobile.com",
    "phone_primary": "+971566130458",
    "phone_secondary": "+971559879422",
    "phone_landline": "+97167317652",
    "whatsapp_number": "971566130458",
    "whatsapp_message": "Hello, I'm interested in your products!",
    "hours": "Mon – Sun · 10:00 – 23:00",
    "ships_to": "UAE & KSA · 2–4 business days",
    "vat_note": "All prices include 5% VAT (Profit Margin Scheme)",
    "return_window_days": 7,
    "social": {
        "tiktok": "https://tiktok.com/@shop216rollamall",
        "instagram": "https://instagram.com/shahzadarshadelect.dev",
        "facebook": "https://facebook.com/profile.php?id=100054487568342",
    },
    "tawk_to_id": "684c4d3cac212a190e45f2b1/1itl0rdtm",
}


def site(request):
    wishlist_ids = set()
    cart_count = 0
    try:
        cart = get_or_create_cart(request)
        cart_count = cart.count
    except Exception:
        pass
    if getattr(request, "user", None) and request.user.is_authenticated:
        wishlist_ids = set(
            WishedProduct.objects.filter(user=request.user).values_list("product_id", flat=True)
        )
    return {
        "SITE_URL": getattr(settings, "SITE_URL", ""),
        "CURRENCY": getattr(settings, "CURRENCY", "AED"),
        "CART_COUNT": cart_count,
        "WISHLIST_IDS": wishlist_ids,
        "BRAND": BRAND,
    }
