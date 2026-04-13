from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Address, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "username", "is_staff", "referral_source", "date_joined")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "city", "country", "is_default")
    list_filter = ("country", "is_default")
    search_fields = ("user__email", "name", "city")
