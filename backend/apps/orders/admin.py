from django.contrib import admin, messages
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("title", "unit_price", "quantity", "line_total")

    def line_total(self, obj):
        if obj.pk:
            return obj.line_total
        return ""


STATUS_COLORS = {
    "pending": "#FEF3C7,#92400E",
    "paid": "#DCFCE7,#166534",
    "shipped": "#DBEAFE,#1E40AF",
    "delivered": "#E0E7FF,#3730A3",
    "cancelled": "#FEE2E2,#991B1B",
    "failed": "#FEE2E2,#991B1B",
}


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("short_ref", "name", "email", "total_display", "payment_method", "status_badge", "paid", "created_at")
    list_filter = ("status", "payment_method", "paid", "created_at")
    search_fields = ("reference", "name", "email", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("reference", "short_ref", "subtotal", "total", "provider_ref", "created_at", "updated_at")
    list_per_page = 30
    save_on_top = True
    fieldsets = (
        ("Order", {"fields": ("reference", "short_ref", "user", "status", "paid")}),
        ("Payment", {"fields": ("payment_method", "provider", "provider_ref", "currency", "subtotal", "total")}),
        ("Customer", {"fields": ("name", "email", "phone")}),
        ("Shipping", {"fields": ("address_line1", "address_line2", "city", "postal_code", "country")}),
        ("Attribution", {"fields": ("referral_source", "referral_other"), "classes": ("collapse",)}),
        ("Line items snapshot", {"fields": ("line_items",), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    actions = ["mark_paid", "mark_shipped", "mark_delivered", "mark_cancelled"]

    def total_display(self, obj):
        return f"{obj.total} {obj.currency}"
    total_display.short_description = "Total"

    def status_badge(self, obj):
        bg, fg = STATUS_COLORS.get(obj.status, "#f3f4f6,#374151").split(",")
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;border-radius:999px;font-size:11px;text-transform:uppercase">{}</span>',
            bg, fg, obj.status,
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark as paid")
    def mark_paid(self, request, queryset):
        n = queryset.update(paid=True, status=Order.Status.PAID)
        self.message_user(request, f"{n} order(s) marked paid.", messages.SUCCESS)

    @admin.action(description="Mark as shipped")
    def mark_shipped(self, request, queryset):
        n = queryset.update(status=Order.Status.SHIPPED)
        self.message_user(request, f"{n} order(s) marked shipped.", messages.SUCCESS)

    @admin.action(description="Mark as delivered")
    def mark_delivered(self, request, queryset):
        n = queryset.update(status=Order.Status.DELIVERED)
        self.message_user(request, f"{n} order(s) marked delivered.", messages.SUCCESS)

    @admin.action(description="Mark as cancelled")
    def mark_cancelled(self, request, queryset):
        n = queryset.update(status=Order.Status.CANCELLED)
        self.message_user(request, f"{n} order(s) cancelled.", messages.SUCCESS)
