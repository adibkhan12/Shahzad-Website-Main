from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("title", "unit_price", "quantity", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("short_ref", "name", "email", "total", "payment_method", "status", "paid", "created_at")
    list_filter = ("status", "payment_method", "paid")
    search_fields = ("reference", "name", "email", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("reference", "created_at", "updated_at")
