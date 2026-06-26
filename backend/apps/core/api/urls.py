from django.urls import path

from .views import CsrfTokenView, SiteConfigView, StaticPageView

urlpatterns = [
    path("csrf/", CsrfTokenView.as_view(), name="csrf-token"),
    path("config/", SiteConfigView.as_view(), name="site-config"),
    path("pages/<slug:slug>/", StaticPageView.as_view(), name="static-page"),
]
