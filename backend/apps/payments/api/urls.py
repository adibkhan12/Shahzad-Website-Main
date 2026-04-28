from django.urls import path

from .views import CancelView, CheckoutView, ConfirmView, webhook

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("confirm/", ConfirmView.as_view(), name="confirm"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("webhook/<str:provider>/", webhook, name="webhook"),
]
