from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("review/<int:product_id>/", views.review_create, name="review_create"),
    path("question/<int:product_id>/", views.question_create, name="question_create"),
]
