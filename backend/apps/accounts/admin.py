from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Address, User


class AddressInline(TabularInline):
    model = Address
    extra = 0
    fields = ("name", "city", "country", "is_default")


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("email", "full_name", "is_staff", "referral_source", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "referral_source")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)
    inlines = [AddressInline]

    def full_name(self, obj):
        return (obj.get_full_name() or "").strip() or "—"


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ("user", "name", "city", "country", "is_default")
    list_filter = ("country", "is_default")
    search_fields = ("user__email", "name", "city")
