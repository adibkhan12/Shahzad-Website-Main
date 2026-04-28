from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html
from import_export import resources
from import_export.fields import Field
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeNumericFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import display

try:
    from import_export.admin import ImportExportModelAdmin
except ImportError:
    ImportExportModelAdmin = ModelAdmin

from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import AdBanner, Brand, Category, HomePage, Product, ProductImage, QA, Review, Setting


# ---------- Import/Export Resource ----------

class ProductResource(resources.ModelResource):
    category = Field(attribute="category__name", column_name="category")
    brand = Field(attribute="brand__name", column_name="brand")

    class Meta:
        model = Product
        fields = (
            "id", "title", "slug", "brand", "category", "price",
            "sale_price", "stock", "is_active", "is_featured", "description",
        )
        export_order = fields
        import_id_fields = ("slug",)

    def before_import_row(self, row, **kwargs):
        cat_name = row.get("category")
        cat = None
        if cat_name:
            cat, _ = Category.objects.get_or_create(name=cat_name)
            row["category"] = cat.pk
        brand_name = row.get("brand")
        if brand_name:
            b, _ = Brand.objects.get_or_create(
                name=brand_name, category=cat,
            )
            row["brand"] = b.pk


# ---------- Inlines ----------

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt", "order", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px" />', obj.image.url)
        return ""


class BrandInline(TabularInline):
    model = Brand
    extra = 0
    fields = ("name", "slug", "is_active", "order")
    prepopulated_fields = {"slug": ("name",)}
    show_change_link = True


# ---------- Category ----------

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("thumb", "name", "parent", "slug", "brand_count", "product_count", "active_toggle", "order")
    list_display_links = ("thumb", "name")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("parent", "is_active")
    inlines = [BrandInline]
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("name", "slug", "parent", "is_active", "order")}),
        ("Image", {"fields": ("image_file", "image"),
                   "description": "Upload a file or paste a URL."}),
        ("Advanced", {"fields": ("properties",), "classes": ("collapse",)}),
    )
    actions = ["activate", "deactivate"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _brands=Count("brands", distinct=True),
            _products=Count("products", distinct=True),
        )

    def thumb(self, obj):
        url = obj.image_url
        if url:
            return format_html('<img src="{}" style="height:36px;width:36px;object-fit:cover;border-radius:6px" />', url)
        return format_html('<div style="height:36px;width:36px;border-radius:6px;background:#f3f4f6"></div>')
    thumb.short_description = ""

    def brand_count(self, obj):
        return obj._brands
    brand_count.short_description = "Brands"
    brand_count.admin_order_field = "_brands"

    def product_count(self, obj):
        return obj._products
    product_count.short_description = "Products"
    product_count.admin_order_field = "_products"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;">ACTIVE</span>')
        return format_html('<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;">INACTIVE</span>')
    active_toggle.short_description = "Status"

    @admin.action(description="Activate selected")
    def activate(self, request, queryset):
        n = queryset.update(is_active=True)
        self.message_user(request, f"{n} activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected")
    def deactivate(self, request, queryset):
        n = queryset.update(is_active=False)
        self.message_user(request, f"{n} deactivated.", messages.SUCCESS)


# ---------- Brand ----------

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ("logo_thumb", "name", "category", "product_count", "active_toggle", "order")
    list_display_links = ("logo_thumb", "name")
    list_editable = ("order",)
    list_filter = ("category", "is_active")
    search_fields = ("name", "description", "category__name")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("name", "slug", "category", "is_active", "order")}),
        ("Branding", {"fields": ("logo", "description")}),
    )
    actions = ["activate", "deactivate"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_products=Count("products"))

    def logo_thumb(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:36px;width:36px;object-fit:contain;border-radius:6px;background:#fff;border:1px solid #eee" />', obj.logo.url)
        return format_html('<div style="height:36px;width:36px;border-radius:6px;background:#f3f4f6;display:flex;align-items:center;justify-content:center;font-size:12px;color:#9ca3af">{}</div>', obj.name[0] if obj.name else "?")
    logo_thumb.short_description = ""

    def product_count(self, obj):
        return obj._products
    product_count.short_description = "Products"
    product_count.admin_order_field = "_products"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;">ACTIVE</span>')
        return format_html('<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;">INACTIVE</span>')
    active_toggle.short_description = "Status"

    @admin.action(description="Activate selected")
    def activate(self, request, queryset):
        n = queryset.update(is_active=True)
        self.message_user(request, f"{n} activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected")
    def deactivate(self, request, queryset):
        n = queryset.update(is_active=False)
        self.message_user(request, f"{n} deactivated.", messages.SUCCESS)


# ---------- Product ----------

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_classes = [ProductResource]

    list_display = (
        "thumb", "title", "brand_display", "category", "price_display",
        "stock_display", "active_toggle", "is_featured", "edit_link",
    )
    list_filter = ("category", "brand", "is_active", "is_featured", ("price", RangeNumericFilter))
    list_filter_submit = True
    search_fields = ("title", "description", "brand__name")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured",)
    list_display_links = ("thumb", "title")
    list_per_page = 30
    autocomplete_fields = ("category", "brand")
    inlines = [ProductImageInline]
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("title", "slug", "description")}),
        ("Hierarchy", {
            "fields": ("category", "brand"),
            "description": "Pick a category first, then a brand. Brands are listed with their linked category in the dropdown.",
        }),
        ("Pricing", {
            "fields": ("price", "sale_price"),
            "description": "Leave <b>Sale price</b> empty for full price. Enter a lower value to put on sale (price will be struck through).",
        }),
        ("Inventory", {"fields": ("stock", "is_active")}),
        ("Display", {"fields": ("is_featured",)}),
        ("Media (legacy URLs)", {"fields": ("images",), "classes": ("collapse",),
                                  "description": "Optional JSON list of external image URLs. Prefer uploading files via the inline below."}),
        ("Variants & properties", {"fields": ("color_variants", "properties"), "classes": ("collapse",)}),
    )
    actions = ["activate", "deactivate", "mark_featured", "unmark_featured",
               "mark_out_of_stock", "restock_default", "clear_sale", "duplicate"]

    def thumb(self, obj):
        url = obj.primary_image
        if url:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;object-fit:cover;border-radius:8px;border:1px solid rgba(0,0,0,0.06)" />', url,
            )
        return format_html('<div style="height:48px;width:48px;border-radius:8px;background:linear-gradient(135deg,#f3f4f6,#e5e7eb);display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:18px">📦</div>')
    thumb.short_description = ""

    def brand_display(self, obj):
        if obj.brand:
            return format_html(
                '<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:#f3e8ff;color:#5b0a99;font-size:11px;font-weight:500">{}</span>',
                obj.brand.name,
            )
        return format_html('<span style="color:#9ca3af;font-size:11px">— no brand —</span>')
    brand_display.short_description = "Brand"
    brand_display.admin_order_field = "brand__name"

    def price_display(self, obj):
        if obj.on_sale:
            try:
                save = float(obj.price) - float(obj.sale_price)
            except Exception:
                save = 0
            # Pre-format the save amount: format_html() escapes args into
            # SafeString, which breaks numeric format codes like {:.0f}.
            save_str = f"{save:.0f}"
            return format_html(
                '<div style="line-height:1.25">'
                '<div><span style="color:#dc2626;font-weight:700">{} AED</span> '
                '<span style="text-decoration:line-through;color:#9ca3af;font-size:11px;margin-left:4px">{}</span></div>'
                '<div style="font-size:10px;color:#047857;font-weight:600">SAVE {} AED</div>'
                '</div>',
                obj.sale_price, obj.price, save_str,
            )
        return format_html('<span style="font-weight:600">{} AED</span>', obj.price)
    price_display.short_description = "Price"
    price_display.admin_order_field = "price"

    def stock_display(self, obj):
        if obj.stock == 0:
            color, bg, label = "#fff", "#7f1d1d", "OUT"
        elif obj.stock < 5:
            color, bg, label = "#b91c1c", "#fef2f2", f"{obj.stock} left"
        else:
            color, bg, label = "#166534", "#dcfce7", f"{obj.stock} in stock"
        return format_html(
            '<span style="background:{};color:{};padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600">{}</span>',
            bg, color, label,
        )
    stock_display.short_description = "Stock"
    stock_display.admin_order_field = "stock"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600">● ACTIVE</span>')
        return format_html('<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600">○ INACTIVE</span>')
    active_toggle.short_description = "Status"
    active_toggle.admin_order_field = "is_active"

    def edit_link(self, obj):
        return format_html(
            '<a href="/admin/catalog/product/{}/change/" style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border-radius:8px;background:#0a0a0a;color:#fff;font-size:11px;font-weight:500;text-decoration:none">'
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
            '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>'
            '</svg>Edit</a>',
            obj.id,
        )
    edit_link.short_description = ""

    # --- bulk actions ---
    @admin.action(description="Activate (show on site)")
    def activate(self, request, queryset):
        n = queryset.update(is_active=True)
        self.message_user(request, f"{n} product(s) activated.", messages.SUCCESS)

    @admin.action(description="Deactivate (hide from site)")
    def deactivate(self, request, queryset):
        n = queryset.update(is_active=False)
        self.message_user(request, f"{n} product(s) deactivated.", messages.SUCCESS)

    @admin.action(description="Mark selected as featured")
    def mark_featured(self, request, queryset):
        n = queryset.update(is_featured=True)
        self.message_user(request, f"{n} featured.", messages.SUCCESS)

    @admin.action(description="Remove featured flag")
    def unmark_featured(self, request, queryset):
        n = queryset.update(is_featured=False)
        self.message_user(request, f"{n} unfeatured.", messages.SUCCESS)

    @admin.action(description="Set stock to 0 (out of stock)")
    def mark_out_of_stock(self, request, queryset):
        n = queryset.update(stock=0)
        self.message_user(request, f"{n} marked out of stock.", messages.SUCCESS)

    @admin.action(description="Restock to 15 units")
    def restock_default(self, request, queryset):
        n = queryset.update(stock=15)
        self.message_user(request, f"{n} restocked.", messages.SUCCESS)

    @admin.action(description="End sale (clear sale price)")
    def clear_sale(self, request, queryset):
        n = queryset.update(sale_price=None)
        self.message_user(request, f"Sale ended for {n} product(s).", messages.SUCCESS)

    @admin.action(description="Duplicate selected products")
    def duplicate(self, request, queryset):
        count = 0
        for p in queryset:
            p.pk = None
            p.slug = ""
            p.title = f"{p.title} (copy)"
            p.save()
            count += 1
        self.message_user(request, f"Duplicated {count} product(s).", messages.SUCCESS)


# ---------- Banners & misc ----------

@admin.register(AdBanner)
class AdBannerAdmin(ModelAdmin):
    list_display = ("title", "thumb", "order", "link", "bg_swatch", "active_toggle")
    list_editable = ("order",)
    list_filter = ("is_active",)
    fieldsets = (
        ("English (default)", {"fields": ("title", "desc", "button")}),
        ("العربية (Arabic)", {
            "fields": ("title_ar", "desc_ar", "button_ar"),
            "description": "Leave blank to fall back to the English copy.",
        }),
        ("Link & status", {"fields": ("link", "is_active")}),
        ("Visual", {"fields": ("image_file", "image", "bg", "order")}),
    )

    def thumb(self, obj):
        url = obj.image_url
        if url:
            return format_html('<img src="{}" style="height:36px;border-radius:4px" />', url)
        return "—"

    def bg_swatch(self, obj):
        return format_html(
            '<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{};vertical-align:middle;border:1px solid rgba(0,0,0,0.1)"></span>'
            ' <code style="font-size:11px">{}</code>', obj.bg, obj.bg,
        )
    bg_swatch.short_description = "Colour"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;">ACTIVE</span>')
        return format_html('<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;">INACTIVE</span>')
    active_toggle.short_description = "Status"


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("product", "user", "rating", "short_text", "created_at")
    list_filter = ("rating",)
    search_fields = ("user", "text", "product__title")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("product",)

    def short_text(self, obj):
        return (obj.text or "")[:80]


@admin.register(QA)
class QAAdmin(ModelAdmin):
    list_display = ("product", "user", "short_q", "answered")
    search_fields = ("user", "question", "answer", "product__title")
    autocomplete_fields = ("product",)
    fieldsets = (
        (None, {"fields": ("product", "user", "question")}),
        ("Answer", {"fields": ("answer", "answered_at")}),
    )

    def short_q(self, obj):
        return obj.question[:80]

    def answered(self, obj):
        return bool(obj.answer)
    answered.boolean = True


@admin.register(Setting)
class SettingAdmin(ModelAdmin):
    list_display = ("name", "updated_at")
    search_fields = ("name",)


@admin.register(HomePage)
class HomePageAdmin(ModelAdmin):
    """Singleton admin page for homepage configuration. Pick a hero product from a dropdown."""

    autocomplete_fields = ("hero_product",)
    fieldsets = (
        ("Hero", {
            "fields": ("hero_product",),
            "description": (
                "Pick the product you want shown as the big hero image on the homepage. "
                "Leave blank to fall back to the most recently featured product."
            ),
        }),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        # Only allow one row ever.
        return not HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Skip the list — jump straight to the singleton's edit page.
        obj = HomePage.load()
        return HttpResponseRedirect(reverse("admin:catalog_homepage_change", args=(obj.pk,)))
