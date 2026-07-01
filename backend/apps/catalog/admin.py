import json

from django import forms
from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html
from import_export import resources
from import_export.fields import Field
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeNumericFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm

try:
    from import_export.admin import ImportExportModelAdmin
except ImportError:
    ImportExportModelAdmin = ModelAdmin

from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import (
    QA,
    AdBanner,
    Brand,
    CatalogProperty,
    Category,
    ColorVariant,
    HomePage,
    Product,
    ProductImage,
    Review,
    Setting,
    StockMovement,
)


# ---------- Custom form widgets ----------


class CommaSeparatedValuesWidget(forms.Textarea):
    """Displays a JSON list as human-readable comma-separated text."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {}).update(
            {"rows": 3, "placeholder": "Red, Blue, Green, ..."}
        )
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return ", ".join(str(v) for v in parsed)
            except Exception:
                pass
        return value or ""


class CatalogPropertyAdminForm(forms.ModelForm):
    property_values = forms.CharField(
        widget=CommaSeparatedValuesWidget,
        required=False,
        label="Values (comma-separated)",
        help_text="Type each allowed value separated by a comma. New values added via products are appended automatically.",
    )

    class Meta:
        model = CatalogProperty
        fields = ["property_name", "property_values"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["property_values"].initial = ", ".join(
                str(v) for v in (self.instance.property_values or [])
            )
        else:
            self.fields["property_values"].initial = ""

    def clean_property_values(self):
        raw = self.cleaned_data.get("property_values", "")
        seen: set[str] = set()
        unique: list[str] = []
        for v in (v.strip() for v in raw.split(",") if v.strip()):
            key = v.lower()
            if key not in seen:
                seen.add(key)
                unique.append(v)
        return unique

# ---------- Import/Export Resource ----------


class ProductResource(resources.ModelResource):
    category = Field(attribute="category__name", column_name="category")
    brand = Field(attribute="brand__name", column_name="brand")

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "brand",
            "category",
            "price",
            "sale_price",
            "stock",
            "is_active",
            "is_featured",
            "description",
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
                name=brand_name,
                category=cat,
            )
            row["brand"] = b.pk


# ---------- Inlines ----------


class ColorVariantInline(TabularInline):
    """One row per color — shows price column only when 'Is price same?' is off (controlled by JS)."""

    model = ColorVariant
    extra = 1
    fields = ("color_name", "price", "order")
    ordering = ("order", "color_name")
    verbose_name = "Color Variant"
    verbose_name_plural = "Color Variants"


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "color_variant", "alt", "order", "preview")
    readonly_fields = ("preview",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "color_variant":
            obj_id = request.resolver_match.kwargs.get("object_id")
            if obj_id:
                kwargs["queryset"] = ColorVariant.objects.filter(product_id=obj_id)
            else:
                kwargs["queryset"] = ColorVariant.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px" />', obj.image.url
            )
        return ""


class StockMovementInline(TabularInline):
    """Read-only audit trail of stock changes shown on the product change page."""

    model = StockMovement
    extra = 0
    can_delete = False
    fields = ("created_at", "delta", "note", "user")
    readonly_fields = ("created_at", "delta", "note", "user")
    ordering = ("-created_at",)

    def has_add_permission(self, request, obj=None):
        return False  # log entries are created automatically


class BrandInline(TabularInline):
    model = Brand
    extra = 0
    fields = ("name", "slug", "is_active", "order")
    prepopulated_fields = {"slug": ("name",)}
    show_change_link = True


# ---------- Category ----------


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "thumb",
        "name",
        "parent",
        "slug",
        "brand_count",
        "product_count",
        "active_toggle",
        "order",
    )
    list_display_links = ("thumb", "name")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    list_filter = ("parent", "is_active")
    inlines = [BrandInline]
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("name", "slug", "parent", "is_active", "order")}),
        (
            "Image",
            {"fields": ("image_file", "image"), "description": "Upload a file or paste a URL."},
        ),
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
            return format_html(
                '<img src="{}" style="height:36px;width:36px;object-fit:cover;border-radius:6px" />',
                url,
            )
        return format_html(
            '<div style="height:36px;width:36px;border-radius:6px;background:#f3f4f6"></div>'
        )

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
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;">INACTIVE</span>'
        )

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
            return format_html(
                '<img src="{}" style="height:36px;width:36px;object-fit:contain;border-radius:6px;background:#fff;border:1px solid #eee" />',
                obj.logo.url,
            )
        return format_html(
            '<div style="height:36px;width:36px;border-radius:6px;background:#f3f4f6;display:flex;align-items:center;justify-content:center;font-size:12px;color:#9ca3af">{}</div>',
            obj.name[0] if obj.name else "?",
        )

    logo_thumb.short_description = ""

    def product_count(self, obj):
        return obj._products

    product_count.short_description = "Products"
    product_count.admin_order_field = "_products"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;">INACTIVE</span>'
        )

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

    class Media:
        js = (
            "catalog/js/product_properties.js",
            "catalog/js/color_variants.js",
        )
        css = {
            "all": (
                "catalog/css/product_properties.css",
                "catalog/css/color_variants.css",
                "catalog/css/product_toggles.css",
            )
        }

    list_display = (
        "thumb",
        "title",
        "brand_display",
        "category",
        "price_display",
        "stock_display",
        "stock",  # editable column — comes after the read-only badge for visual context
        "active_toggle",
        "is_featured",
        "edit_link",
    )
    list_filter = ("category", "brand", "is_active", "is_featured", ("price", RangeNumericFilter))
    list_filter_submit = True
    search_fields = ("title", "description", "brand__name")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("stock", "is_featured")
    list_display_links = ("thumb", "title")
    list_per_page = 30
    autocomplete_fields = ("category", "brand")
    inlines = [ColorVariantInline, ProductImageInline, StockMovementInline]
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("title", "slug", "description")}),
        ("Hierarchy", {"fields": ("category", "brand")}),
        (
            "Pricing",
            {
                "fields": ("price", "sale_price"),
                "description": "Leave <b>Sale price</b> empty for full price.",
            },
        ),
        ("Inventory", {"fields": ("stock",)}),
        (
            "Options",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                    "is_box_packed",
                    "has_color_variants",
                    "is_price_same",
                ),
                "classes": ("product-toggles",),
            },
        ),
        (
            "Media (legacy URLs)",
            {
                "fields": ("images",),
                "classes": ("collapse",),
                "description": "Optional JSON list of external image URLs. Prefer uploading files via the inline below.",
            },
        ),
        (
            "Product Properties",
            {
                "fields": ("product_properties",),
                "description": (
                    "Use <strong>＋ Add Property</strong> to pick an existing global property "
                    "or type a brand-new name to create one. Values auto-complete from the "
                    "<a href='/admin/catalog/catalogproperty/'>Properties</a> registry."
                ),
            },
        ),
    )
    actions = [
        "change_stock_by",
        "activate",
        "deactivate",
        "mark_featured",
        "unmark_featured",
        "mark_out_of_stock",
        "restock_default",
        "clear_sale",
        "duplicate",
    ]

    _TOGGLE_FIELDS = ('is_active', 'is_featured', 'is_box_packed', 'has_color_variants', 'is_price_same')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for name in self._TOGGLE_FIELDS:
            if name in form.base_fields:
                form.base_fields[name].help_text = ''
        return form

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom = [
            path(
                '<int:product_id>/save-color-variants/',
                self.admin_site.admin_view(self.save_color_variants_view),
                name='catalog_product_save_color_variants',
            ),
        ]
        return custom + urls

    def save_color_variants_view(self, request, product_id):
        """AJAX endpoint — saves only the color variant inline without touching the rest of the product form."""
        if request.method != 'POST':
            return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)
        product = get_object_or_404(Product, pk=product_id)
        ColorVariantFormSet = inlineformset_factory(
            Product,
            ColorVariant,
            fields=('color_name', 'price', 'order'),
            extra=0,
            can_delete=True,
        )
        formset = ColorVariantFormSet(
            request.POST,
            instance=product,
            prefix='color_variants_data',
        )
        if formset.is_valid():
            formset.save()
            variants = list(
                ColorVariant.objects.filter(product=product)
                .order_by('order', 'color_name')
                .values('id', 'color_name')
            )
            return JsonResponse({'ok': True, 'variants': variants})
        non_empty_errors = [e for e in formset.errors if e]
        return JsonResponse({'ok': False, 'errors': non_empty_errors}, status=400)

    def save_model(self, request, obj, form, change):
        """Log stock changes and back-propagate new property values to CatalogProperty."""
        # Keep the 'Type' property in sync with is_box_packed before saving.
        if not isinstance(obj.product_properties, dict):
            obj.product_properties = {}
        obj.product_properties['Type'] = 'Box-packed' if obj.is_box_packed else 'Used'

        delta = 0
        if change and obj.pk:
            try:
                old_stock = Product.objects.values_list("stock", flat=True).get(pk=obj.pk)
                delta = obj.stock - old_stock
            except Product.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)
        if delta != 0:
            StockMovement.objects.create(
                product=obj,
                delta=delta,
                note="Inline edit via admin",
                user=request.user if request.user.is_authenticated else None,
            )
        # Auto-expand CatalogProperty.property_values with any newly typed values.
        if isinstance(obj.product_properties, dict):
            for prop_name, prop_value in obj.product_properties.items():
                if not prop_name or not prop_value:
                    continue
                prop, _ = CatalogProperty.objects.get_or_create(property_name=prop_name)
                str_value = str(prop_value).strip()
                if str_value and str_value not in prop.property_values:
                    prop.property_values.append(str_value)
                    prop.save(update_fields=["property_values"])

    def thumb(self, obj):
        url = obj.primary_image
        if url:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;object-fit:cover;border-radius:8px;border:1px solid rgba(0,0,0,0.06)" />',
                url,
            )
        return format_html(
            '<div style="height:48px;width:48px;border-radius:8px;background:linear-gradient(135deg,#f3f4f6,#e5e7eb);display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:18px">📦</div>'
        )

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
                "</div>",
                obj.sale_price,
                obj.price,
                save_str,
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
            bg,
            color,
            label,
        )

    stock_display.short_description = "Stock"
    stock_display.admin_order_field = "stock"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600">● ACTIVE</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600">○ INACTIVE</span>'
        )

    active_toggle.short_description = "Status"
    active_toggle.admin_order_field = "is_active"

    def edit_link(self, obj):
        return format_html(
            '<a href="/admin/catalog/product/{}/change/" style="display:inline-flex;align-items:center;gap:4px;padding:4px 10px;border-radius:8px;background:#0a0a0a;color:#fff;font-size:11px;font-weight:500;text-decoration:none">'
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>'
            '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>'
            "</svg>Edit</a>",
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
        n = 0
        for product in queryset.exclude(stock=0):
            delta = -product.stock
            product.stock = 0
            product.save(update_fields=["stock"])
            StockMovement.objects.create(
                product=product,
                delta=delta,
                note="Marked out of stock via bulk action",
                user=request.user if request.user.is_authenticated else None,
            )
            n += 1
        self.message_user(request, f"{n} marked out of stock.", messages.SUCCESS)

    @admin.action(description="Restock to 15 units")
    def restock_default(self, request, queryset):
        n = 0
        for product in queryset:
            if product.stock == 15:
                continue
            delta = 15 - product.stock
            product.stock = 15
            product.save(update_fields=["stock"])
            StockMovement.objects.create(
                product=product,
                delta=delta,
                note="Restocked to default (15) via bulk action",
                user=request.user if request.user.is_authenticated else None,
            )
            n += 1
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

    @admin.action(description="📦 Adjust stock by N (received / damaged / count fix)")
    def change_stock_by(self, request, queryset):
        """
        Two-step bulk action:
        1) First call (no `apply` flag) — render an intermediate form asking
           for delta + optional note, listing the selected products.
        2) Second call (`apply=1`) — apply the delta to every selected
           product, log a StockMovement per product, and return to changelist.
        """
        if request.POST.get("apply") == "1":
            try:
                delta = int(request.POST.get("delta", "0"))
            except ValueError:
                delta = 0
            note = (request.POST.get("note") or "").strip()
            if delta == 0:
                self.message_user(request, "Delta was 0 — nothing changed.", messages.WARNING)
                return None
            updated = 0
            for product in queryset:
                product.stock = max(0, product.stock + delta)
                product.save(update_fields=["stock"])
                StockMovement.objects.create(
                    product=product,
                    delta=delta,
                    note=note or "Bulk stock adjustment",
                    user=request.user if request.user.is_authenticated else None,
                )
                updated += 1
            sign = "+" if delta > 0 else ""
            self.message_user(
                request,
                f"Adjusted stock by {sign}{delta} for {updated} product(s).",
                messages.SUCCESS,
            )
            return None  # redirect back to changelist

        # First call: render the intermediate form.
        return render(
            request,
            "admin/catalog/change_stock_form.html",
            {
                "title": "Adjust stock",
                "products": queryset,
                "selected_pks": [str(pk) for pk in queryset.values_list("pk", flat=True)],
                "opts": self.model._meta,
            },
        )


# ---------- CatalogProperty ----------


@admin.register(CatalogProperty)
class CatalogPropertyAdmin(ModelAdmin):
    """Global property name + allowed-values registry.

    The 'Values' textarea accepts a comma-separated list.  New values typed
    into product forms are appended here automatically when a product is saved.
    """

    form = CatalogPropertyAdminForm
    list_display = ("property_name", "values_preview", "value_count")
    search_fields = ("property_name",)
    save_on_top = True
    fieldsets = (
        (
            None,
            {
                "fields": ("property_name", "property_values"),
                "description": (
                    "Add a new property name (e.g. <strong>Color</strong>) and the values "
                    "that are globally allowed for it.  Values entered on the product form "
                    "are appended here automatically."
                ),
            },
        ),
    )

    def values_preview(self, obj):
        vals = obj.property_values or []
        chips = "".join(
            format_html(
                '<span style="display:inline-block;padding:1px 8px;margin:1px;border-radius:999px;'
                'background:#f3e8ff;color:#5b0a99;font-size:11px">{}</span>',
                v,
            )
            for v in vals[:8]
        )
        more = f" +{len(vals)-8} more" if len(vals) > 8 else ""
        return format_html("{}{}", chips, more)

    values_preview.short_description = "Allowed values"

    def value_count(self, obj):
        return len(obj.property_values or [])

    value_count.short_description = "# Values"


# ---------- Banners & misc ----------


@admin.register(AdBanner)
class AdBannerAdmin(ModelAdmin):
    list_display = ("title", "thumb", "order", "link", "bg_swatch", "active_toggle")
    list_editable = ("order",)
    list_filter = ("is_active",)
    fieldsets = (
        ("English (default)", {"fields": ("title", "desc", "button")}),
        (
            "العربية (Arabic)",
            {
                "fields": ("title_ar", "desc_ar", "button_ar"),
                "description": "Leave blank to fall back to the English copy.",
            },
        ),
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
            ' <code style="font-size:11px">{}</code>',
            obj.bg,
            obj.bg,
        )

    bg_swatch.short_description = "Colour"

    def active_toggle(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 10px;border-radius:999px;font-size:11px;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:999px;font-size:11px;">INACTIVE</span>'
        )

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


@admin.register(StockMovement)
class StockMovementAdmin(ModelAdmin):
    """
    Top-level view of every stock adjustment ever made via the admin.
    Read-only — adjustments happen via the Product list / Product page,
    and they auto-create rows here.
    """

    list_display = ("created_at", "product", "delta_badge", "note", "user")
    list_filter = ("user", "created_at")
    search_fields = ("product__title", "note", "user__email")
    readonly_fields = ("product", "delta", "note", "user", "created_at")
    date_hierarchy = "created_at"
    list_per_page = 50
    autocomplete_fields = ("product",)

    def delta_badge(self, obj):
        if obj.delta > 0:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 10px;'
                'border-radius:999px;font-size:11px;font-weight:600">+{}</span>',
                obj.delta,
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;padding:2px 10px;'
            'border-radius:999px;font-size:11px;font-weight:600">{}</span>',
            obj.delta,
        )

    delta_badge.short_description = "Delta"
    delta_badge.admin_order_field = "delta"

    def has_add_permission(self, request):
        return False  # only auto-created via Product save / bulk action

    def has_change_permission(self, request, obj=None):
        return False  # immutable audit log

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomePage)
class HomePageAdmin(ModelAdmin):
    """Singleton admin page for homepage configuration. Pick a hero product from a dropdown."""

    autocomplete_fields = ("hero_product",)
    fieldsets = (
        (
            "Hero",
            {
                "fields": ("hero_product",),
                "description": (
                    "Pick the product you want shown as the big hero image on the homepage. "
                    "Leave blank to fall back to the most recently featured product."
                ),
            },
        ),
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
