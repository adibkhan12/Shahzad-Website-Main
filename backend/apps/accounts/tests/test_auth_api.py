"""Tests for the auth API: login, register, Google sign-in."""
from unittest.mock import patch

import pytest

from apps.accounts.models import User


@pytest.mark.django_db
class TestLogin:
    URL = "/api/v1/auth/login/"

    def test_valid_credentials_returns_jwt(self, api_client, user):
        response = api_client.post(self.URL, {"email": user.email, "password": "TestPass123!"})

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["email"] == user.email

    def test_invalid_password_returns_401(self, api_client, user):
        response = api_client.post(self.URL, {"email": user.email, "password": "WrongPass"})

        assert response.status_code == 401

    def test_unknown_email_returns_401(self, api_client):
        response = api_client.post(
            self.URL, {"email": "ghost@nowhere.com", "password": "anything"}
        )

        assert response.status_code == 401

    def test_email_match_is_case_insensitive(self, api_client, user):
        response = api_client.post(
            self.URL, {"email": user.email.upper(), "password": "TestPass123!"}
        )

        assert response.status_code == 200


@pytest.mark.django_db
class TestRegister:
    URL = "/api/v1/auth/register/"

    def test_creates_user_and_returns_jwt(self, api_client):
        response = api_client.post(
            self.URL,
            {
                "email": "newuser@example.com",
                "password": "StrongPass123!",
                "first_name": "New",
                "last_name": "User",
            },
        )

        assert response.status_code == 201
        assert "access" in response.data
        user = User.objects.get(email="newuser@example.com")
        assert user.first_name == "New"
        assert user.check_password("StrongPass123!")

    def test_rejects_duplicate_email(self, api_client, user):
        response = api_client.post(
            self.URL, {"email": user.email, "password": "AnotherPass123!"}
        )

        assert response.status_code == 400

    def test_rejects_short_password(self, api_client):
        response = api_client.post(
            self.URL,
            {"email": "shortpass@example.com", "password": "abc"},
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestGoogleAuth:
    URL = "/api/v1/auth/google/"

    def test_creates_new_user_from_google_payload(self, api_client, settings):
        settings.GOOGLE_OAUTH_CLIENT_ID = "test-client-id"
        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {
                "email": "googleuser@gmail.com",
                "given_name": "Google",
                "family_name": "Person",
            }
            response = api_client.post(self.URL, {"id_token": "valid-fake-token"})

        assert response.status_code == 200
        assert "access" in response.data
        user = User.objects.get(email="googleuser@gmail.com")
        assert user.first_name == "Google"
        assert user.last_name == "Person"
        assert not user.has_usable_password()  # Google-created users get unusable password

    def test_signs_in_existing_user_without_creating_duplicate(
        self, api_client, user, settings
    ):
        settings.GOOGLE_OAUTH_CLIENT_ID = "test-client-id"
        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.return_value = {"email": user.email, "given_name": "X", "family_name": "Y"}
            response = api_client.post(self.URL, {"id_token": "valid-fake-token"})

        assert response.status_code == 200
        # No duplicate created
        assert User.objects.filter(email=user.email).count() == 1
        assert response.data["user"]["email"] == user.email

    def test_invalid_token_returns_401(self, api_client, settings):
        settings.GOOGLE_OAUTH_CLIENT_ID = "test-client-id"
        with patch("google.oauth2.id_token.verify_oauth2_token") as mock_verify:
            mock_verify.side_effect = ValueError("Invalid token signature")
            response = api_client.post(self.URL, {"id_token": "bogus-token"})

        assert response.status_code == 401

    def test_returns_503_when_oauth_not_configured(self, api_client, settings):
        settings.GOOGLE_OAUTH_CLIENT_ID = ""

        response = api_client.post(self.URL, {"id_token": "anything"})

        assert response.status_code == 503

    def test_rejects_payload_without_id_token(self, api_client, settings):
        settings.GOOGLE_OAUTH_CLIENT_ID = "test-client-id"

        response = api_client.post(self.URL, {})

        assert response.status_code == 400
