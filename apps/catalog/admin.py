from django.contrib import admin

from .models import AdBanner, Category, Product, QA, Review, Setting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "stock", "category", "brand", "is_featured", "created_at")
    list_filter = ("category", "brand", "is_featured")
    search_fields = ("title", "description", "brand")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "stock", "is_featured")


@admin.register(AdBanner)
class AdBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "link", "bg")
    list_editable = ("order",)


admin.site.register(Review)
admin.site.register(QA)
admin.site.register(Setting)
