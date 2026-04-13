from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("track/", views.track, name="track"),
    path("<uuid:reference>/", views.order_detail, name="detail"),
]
