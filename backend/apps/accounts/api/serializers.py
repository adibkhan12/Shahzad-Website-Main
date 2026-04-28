from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import Address

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "full_name", "date_joined", "referral_source", "referral_other",
        ]
        read_only_fields = ["id", "email", "username", "date_joined"]

    def get_full_name(self, obj):
        return (obj.get_full_name() or "").strip()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    referral_source = serializers.CharField(required=False, allow_blank=True)
    referral_other = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = User(
            email=email,
            username=email,
            **validated_data,
        )
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "name", "email", "phone", "address_line1", "address_line2",
            "city", "postal_code", "country", "is_default", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
