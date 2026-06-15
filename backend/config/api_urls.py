from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.accounts.api.auth_urls")),
    path("accounts/", include("apps.accounts.api.urls")),
    path("catalog/", include("apps.catalog.api.urls")),
    path("cart/", include("apps.cart.api.urls")),
    path("orders/", include("apps.orders.api.urls")),
    path("payments/", include("apps.payments.api.urls")),
    path("coupons/", include("apps.coupons.api.urls")),
    path("repairs/", include("apps.repairs.api.urls")),
    path("wishlist/", include("apps.wishlist.api.urls")),
    path("core/", include("apps.core.api.urls")),
]
