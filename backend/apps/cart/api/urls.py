from django.urls import path

from .views import CartAddView, CartClearView, CartItemView, CartMergeView, CartView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", CartAddView.as_view(), name="cart-add"),
    path("items/<int:item_id>/", CartItemView.as_view(), name="cart-item"),
    path("clear/", CartClearView.as_view(), name="cart-clear"),
    path("merge/", CartMergeView.as_view(), name="cart-merge"),
]
