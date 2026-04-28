from rest_framework.routers import DefaultRouter

from .views import BannerViewSet, BrandViewSet, CategoryViewSet, ProductViewSet, SettingViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"brands", BrandViewSet, basename="brand")
router.register(r"banners", BannerViewSet, basename="banner")
router.register(r"settings", SettingViewSet, basename="setting")

urlpatterns = router.urls
