from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import WishedProduct


@admin.register(WishedProduct)
class WishedProductAdmin(ModelAdmin):
    list_display = ("thumb", "product", "user", "added_at")
    list_display_links = ("thumb", "product")
    list_filter = ("added_at",)
    search_fields = ("user__email", "user__username", "product__title", "product__slug")
    readonly_fields = ("added_at",)
    autocomplete_fields = ("user", "product")
    date_hierarchy = "added_at"
    list_per_page = 50

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related("user", "product", "product__brand")
        )

    def thumb(self, obj):
        url = obj.product.primary_image if obj.product else None
        if url:
            return format_html(
                '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px" />',
                url,
            )
        return format_html(
            '<div style="height:40px;width:40px;border-radius:6px;'
            'background:linear-gradient(135deg,#f3f4f6,#e5e7eb);display:flex;'
            'align-items:center;justify-content:center;color:#9ca3af;font-size:14px">♡</div>'
        )
    thumb.short_description = ""
