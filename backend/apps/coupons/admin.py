from django.contrib import admin

from .models import Coupon, CouponRedemption


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_display",
        "region_scope",
        "min_subtotal",
        "used_count",
        "usage_limit",
        "is_active",
        "valid_from",
        "valid_until",
    )
    list_filter = ("is_active", "region_scope", "discount_type")
    search_fields = ("code", "description")
    filter_horizontal = ("applies_to_categories", "applies_to_brands")
    readonly_fields = ("used_count", "created_at", "updated_at")

    fieldsets = (
        (
            "Code & status",
            {"fields": ("code", "description", "is_active")},
        ),
        (
            "Discount",
            {
                "fields": (
                    "discount_type",
                    "discount_value",
                    "max_discount",
                    "min_subtotal",
                ),
                "description": (
                    "Percent: enter 10 for 10% off. Fixed: enter 50 for AED 50 off. "
                    "Use max_discount to cap percentage coupons (e.g. 10% off up to AED 100)."
                ),
            },
        ),
        (
            "Scope",
            {
                "fields": (
                    "region_scope",
                    "applies_to_categories",
                    "applies_to_brands",
                ),
                "description": (
                    "Leave categories and brands empty to apply to the whole catalogue."
                ),
            },
        ),
        (
            "Validity & limits",
            {
                "fields": (
                    "valid_from",
                    "valid_until",
                    "usage_limit",
                    "per_user_limit",
                    "used_count",
                )
            },
        ),
        ("Bookkeeping", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Discount")
    def discount_display(self, obj):
        if obj.discount_type == Coupon.DiscountType.PERCENT:
            cap = f" (cap AED {obj.max_discount:.0f})" if obj.max_discount else ""
            return f"{obj.discount_value:.0f}% off{cap}"
        return f"AED {obj.discount_value:.0f} off"


@admin.register(CouponRedemption)
class CouponRedemptionAdmin(admin.ModelAdmin):
    list_display = ("coupon", "user", "order", "discount_amount", "created_at")
    list_filter = ("coupon",)
    search_fields = ("coupon__code", "user__email", "order__reference")
    readonly_fields = ("coupon", "user", "order", "discount_amount", "created_at")

    def has_add_permission(self, request):
        return False
