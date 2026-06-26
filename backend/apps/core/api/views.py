from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.api.serializers import AdBannerSerializer
from apps.catalog.models import AdBanner, Setting


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class SiteConfigView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        settings_qs = Setting.objects.all()
        settings_data = {s.name: s.value for s in settings_qs}
        banners = AdBanner.objects.all()[:6]
        return Response(
            {
                "settings": settings_data,
                "banners": AdBannerSerializer(banners, many=True).data,
            }
        )


_STATIC_PAGES = {
    "about": {
        "title": "About Shahzad",
        "body": (
            "Shahzad Mobile & Electronics is a Dubai-based specialist in second-hand and refurbished "
            "smartphones, laptops and accessories. We resell quality pre-owned devices — every unit is "
            "inspected, tested, and backed by a warranty.\n\n"
            "We also buy devices. Bring your old phone, laptop, or tablet to our Dubai flagship for a "
            "fair, no-obligation cash quote. No shipping, no forms — just walk in.\n\n"
            "Repairs are all handled on-site by our own certified technicians. Screens, batteries, "
            "water damage, data recovery — walk in and, in most cases, walk out the same day."
        ),
    },
    "support": {
        "title": "Support",
        "body": (
            "The fastest way to reach us is WhatsApp. For in-person help, visit our flagship in Rolla, Sharjah.\n\n"
            "For order help, email support@shahzad.ae or tap the WhatsApp button in the bottom-right."
        ),
    },
    "terms": {
        "title": "Terms & Conditions",
        "body": (
            "All second-hand and refurbished devices come with a written warranty. Returns accepted "
            "within 7 days of purchase for unopened accessories. Repairs carry a 1-year workmanship "
            "warranty on the part replaced.\n\n"
            "Trade-in quotes are valid for 24 hours, subject to in-store inspection."
        ),
    },
}


class StaticPageView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        page = _STATIC_PAGES.get(slug)
        if not page:
            return Response({"detail": "Not found."}, status=404)
        return Response({"slug": slug, **page})
