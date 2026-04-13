from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name="page"),
    path("add/<int:product_id>/", views.add, name="add"),
    path("update/<int:item_id>/", views.update, name="update"),
    path("remove/<int:item_id>/", views.remove, name="remove"),
    path("clear/", views.clear, name="clear"),
    path("badge/", views.badge, name="badge"),
]
