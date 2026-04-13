from django.contrib import admin

from .models import RepairBooking, RepairService


@admin.register(RepairService)
class RepairServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "device", "base_price", "est_minutes", "is_featured", "order")
    list_filter = ("device", "is_featured")
    list_editable = ("base_price", "est_minutes", "is_featured", "order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(RepairBooking)
class RepairBookingAdmin(admin.ModelAdmin):
    list_display = ("short_ref", "name", "device_brand", "device_model", "service", "status", "quoted_price", "created_at")
    list_filter = ("status", "service")
    list_editable = ("status", "quoted_price")
    search_fields = ("reference", "name", "email", "phone", "device_model")
    readonly_fields = ("reference", "created_at", "updated_at")
