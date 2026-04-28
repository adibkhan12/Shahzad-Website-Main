from django.urls import path

from .views import SiteConfigView, StaticPageView

urlpatterns = [
    path("config/", SiteConfigView.as_view(), name="site-config"),
    path("pages/<slug:slug>/", StaticPageView.as_view(), name="static-page"),
]
