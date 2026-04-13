from django.urls import path

from . import views

app_name = "wishlist"

urlpatterns = [
    path("", views.page, name="page"),
    path("toggle/<int:product_id>/", views.toggle, name="toggle"),
]
