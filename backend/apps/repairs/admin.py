from django.contrib import admin, messages
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import RepairBooking, RepairService


@admin.register(RepairService)
class RepairServiceAdmin(ModelAdmin):
    list_display = ("icon_display", "name", "device", "base_price", "est_minutes", "is_featured", "order")
    list_filter = ("device", "is_featured")
    list_editable = ("base_price", "est_minutes", "is_featured", "order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ("name",)

    def icon_display(self, obj):
        return format_html('<span style="font-size:22px">{}</span>', obj.icon or "🔧")
    icon_display.short_description = ""


STATUS_COLORS = {
    "requested": "#FEF3C7,#92400E",
    "quoted": "#DBEAFE,#1E40AF",
    "in_progress": "#E0E7FF,#3730A3",
    "ready": "#DCFCE7,#166534",
    "completed": "#F3F4F6,#374151",
    "cancelled": "#FEE2E2,#991B1B",
}


@admin.register(RepairBooking)
class RepairBookingAdmin(ModelAdmin):
    list_display = ("short_ref", "name", "device_brand", "device_model", "service", "status_badge", "quoted_price", "created_at")
    list_filter = ("status", "service")
    list_editable = ("quoted_price",)
    search_fields = ("reference", "name", "email", "phone", "device_model")
    readonly_fields = ("reference", "short_ref", "created_at", "updated_at")
    actions = ["mark_quoted", "mark_in_progress", "mark_ready", "mark_completed"]

    def status_badge(self, obj):
        bg, fg = STATUS_COLORS.get(obj.status, "#f3f4f6,#374151").split(",")
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;border-radius:999px;font-size:11px;text-transform:uppercase">{}</span>',
            bg, fg, obj.get_status_display(),
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark as quoted")
    def mark_quoted(self, request, queryset):
        n = queryset.update(status=RepairBooking.Status.QUOTED)
        self.message_user(request, f"{n} booking(s) marked quoted.", messages.SUCCESS)

    @admin.action(description="Mark as in progress")
    def mark_in_progress(self, request, queryset):
        n = queryset.update(status=RepairBooking.Status.IN_PROGRESS)
        self.message_user(request, f"{n} booking(s) in progress.", messages.SUCCESS)

    @admin.action(description="Mark as ready for pickup")
    def mark_ready(self, request, queryset):
        n = queryset.update(status=RepairBooking.Status.READY)
        self.message_user(request, f"{n} booking(s) ready.", messages.SUCCESS)

    @admin.action(description="Mark as completed")
    def mark_completed(self, request, queryset):
        n = queryset.update(status=RepairBooking.Status.COMPLETED)
        self.message_user(request, f"{n} booking(s) completed.", messages.SUCCESS)
