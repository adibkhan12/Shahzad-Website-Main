from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, MeView

router = DefaultRouter()
router.register(r"addresses", AddressViewSet, basename="address")

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
