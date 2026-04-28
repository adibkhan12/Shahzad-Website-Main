from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import GoogleAuthView, LoginView, PasswordChangeView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("google/", GoogleAuthView.as_view(), name="auth-google"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("verify/", TokenVerifyView.as_view(), name="auth-verify"),
    path("password/change/", PasswordChangeView.as_view(), name="auth-password-change"),
]
