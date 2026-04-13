from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("return/<str:provider>/<uuid:reference>/success/", views.return_success, name="return_success"),
    path("return/<str:provider>/<uuid:reference>/cancel/", views.return_cancel, name="return_cancel"),
    path("webhook/<str:provider>/", views.webhook, name="webhook"),
    path("thank-you/<uuid:reference>/", views.thank_you, name="thank_you"),
]
