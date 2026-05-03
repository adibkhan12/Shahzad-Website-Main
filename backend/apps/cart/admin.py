from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Cart, CartItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("added_at",)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ("id", "user", "session_key", "count_display", "subtotal_display", "updated_at")
    search_fields = ("user__email", "session_key")
    inlines = [CartItemInline]

    def count_display(self, obj):
        return obj.count

    count_display.short_description = "Items"

    def subtotal_display(self, obj):
        return obj.subtotal

    subtotal_display.short_description = "Subtotal"
