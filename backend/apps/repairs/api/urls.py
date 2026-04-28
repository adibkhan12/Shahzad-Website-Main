from rest_framework.routers import DefaultRouter

from .views import RepairBookingViewSet, RepairServiceViewSet

router = DefaultRouter()
router.register(r"services", RepairServiceViewSet, basename="repair-service")
router.register(r"bookings", RepairBookingViewSet, basename="repair-booking")

urlpatterns = router.urls
