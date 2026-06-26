from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Address
from apps.cart.services import merge_guest_cart_into_user, normalize_guest_session_key

from .serializers import (
    AddressSerializer,
    GoogleAuthSerializer,
    PasswordChangeSerializer,
    RegisterSerializer,
    UserSerializer,
)

User = get_user_model()


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def _merge_guest_cart(request, user):
    session_key = request.data.get("session_key") or request.headers.get("X-Guest-Session")
    session_key = normalize_guest_session_key(session_key)
    if session_key:
        merge_guest_cart_into_user(user, session_key)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        _merge_guest_cart(request, user)
        return Response(
            {"user": UserSerializer(user).data, **_tokens_for(user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        user = authenticate(request, username=email, password=password)
        if user is None:
            try:
                existing = User.objects.get(email__iexact=email)
                user = authenticate(request, username=existing.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is None or not user.is_active:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        _merge_guest_cart(request, user)
        return Response({"user": UserSerializer(user).data, **_tokens_for(user)})


class GoogleAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = GoogleAuthSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        from google.auth.transport import requests as g_requests
        from google.oauth2 import id_token as g_id_token

        client_id = settings.GOOGLE_OAUTH_CLIENT_ID
        if not client_id:
            return Response({"detail": "Google OAuth is not configured."}, status=503)
        try:
            info = g_id_token.verify_oauth2_token(
                ser.validated_data["id_token"], g_requests.Request(), client_id
            )
        except ValueError:
            return Response(
                {"detail": "Invalid Google ID token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        email = (info.get("email") or "").lower()
        if not email:
            return Response({"detail": "Google account has no email."}, status=400)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": info.get("given_name", "") or "",
                "last_name": info.get("family_name", "") or "",
            },
        )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        _merge_guest_cart(request, user)
        return Response({"user": UserSerializer(user).data, **_tokens_for(user)})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        ser = UserSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = PasswordChangeSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(ser.validated_data["old_password"]):
            return Response({"detail": "Current password is incorrect."}, status=400)
        user.set_password(ser.validated_data["new_password"])
        user.save()
        return Response(_tokens_for(user))


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        address = serializer.save(user=self.request.user)
        if address.is_default:
            Address.objects.filter(user=self.request.user).exclude(pk=address.pk).update(
                is_default=False
            )

    def perform_update(self, serializer):
        address = serializer.save()
        if address.is_default:
            Address.objects.filter(user=self.request.user).exclude(pk=address.pk).update(
                is_default=False
            )

    @action(detail=True, methods=["post"])
    def make_default(self, request, pk=None):
        address = self.get_object()
        Address.objects.filter(user=request.user).update(is_default=False)
        address.is_default = True
        address.save(update_fields=["is_default"])
        return Response(self.get_serializer(address).data)
