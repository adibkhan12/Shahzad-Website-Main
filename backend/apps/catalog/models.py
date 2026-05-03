from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children"
    )
    image = models.URLField(blank=True)
    image_file = models.ImageField(upload_to="categories/", blank=True, null=True)
    properties = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["order", "name"]

    @property
    def image_url(self) -> str:
        if self.image_file:
            try:
                return self.image_file.url
            except Exception:
                return ""
        return self.image or ""

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:category_detail", args=[self.slug])

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="brands",
        help_text="Optional: if set, this brand appears under this category in the hierarchy.",
    )
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "category"], name="unique_brand_per_category"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 2
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def logo_url(self):
        if self.logo:
            try:
                return self.logo.url
            except Exception:
                return ""
        return ""

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Regular price (shown struck-through when sale_price is set).",
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional discounted price. If set and lower than price, the product is shown as on sale.",
    )

    images = models.JSONField(default=list, blank=True)
    stock = models.PositiveIntegerField(default=0)
    color_variants = models.JSONField(default=list, blank=True)
    properties = models.JSONField(default=dict, blank=True)

    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="products"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from storefront without deleting.",
    )
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_active"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.slug])

    @property
    def effective_price(self):
        if self.sale_price and self.sale_price < self.price:
            return self.sale_price
        return self.price

    @property
    def on_sale(self):
        return bool(self.sale_price and self.sale_price < self.price)

    @property
    def all_images(self) -> list[str]:
        uploaded = [img.image.url for img in self.uploaded_images.all() if img.image]
        urls = list(self.images or [])
        return uploaded + urls

    @property
    def primary_image(self):
        uploaded = self.uploaded_images.first()
        if uploaded and uploaded.image:
            try:
                return uploaded.image.url
            except Exception:
                pass
        return self.images[0] if self.images else ""

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="uploaded_images")
    image = models.ImageField(upload_to="products/")
    alt = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.product.title} image"


class StockMovement(models.Model):
    """
    Audit log of every admin-initiated stock change (received from supplier,
    damaged, manual count correction, etc.). Every stock change made through
    the admin — inline list edit, bulk action, or change page — leaves a row
    here with the user, delta, and an optional note.

    Sales are NOT logged here — they're already visible via Orders.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_movements")
    delta = models.IntegerField(help_text="Positive for restock, negative for damaged/correction.")
    note = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="stock_movements",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Stock movement"
        verbose_name_plural = "Stock movements"

    def __str__(self):
        sign = "+" if self.delta >= 0 else ""
        return f"{self.product.title} {sign}{self.delta}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.CharField(max_length=120)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField(blank=True)
    images = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class QA(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="qas")
    user = models.CharField(max_length=120)
    question = models.TextField()
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


class Setting(models.Model):
    name = models.CharField(max_length=120, unique=True)
    value = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site config entry"
        verbose_name_plural = "Site config"

    def __str__(self):
        return self.name


class HomePage(models.Model):
    """Singleton row that stores homepage-level selections (currently just the hero product)."""

    hero_product = models.ForeignKey(
        "Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_active": True},
        related_name="+",
        help_text="Shown as the big hero image on the homepage. Pick any active product.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage"
        verbose_name_plural = "Homepage"

    def __str__(self):
        return "Homepage"

    def save(self, *args, **kwargs):
        self.pk = 1  # force singleton
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Singleton: refuse deletion so the row is always available.
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AdBanner(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=300, blank=True)
    button = models.CharField(max_length=80, blank=True)
    # Arabic variants — optional; when empty, the API falls back to the English
    # field above. Edit these in the admin alongside the English copy.
    title_ar = models.CharField(max_length=200, blank=True)
    desc_ar = models.CharField(max_length=300, blank=True)
    button_ar = models.CharField(max_length=80, blank=True)
    image = models.URLField(blank=True)
    image_file = models.ImageField(upload_to="banners/", blank=True, null=True)
    link = models.CharField(max_length=300, blank=True)
    bg = models.CharField(max_length=40, default="#740DC2")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    @property
    def image_url(self) -> str:
        if self.image_file:
            try:
                return self.image_file.url
            except Exception:
                return ""
        return self.image or ""

    def __str__(self):
        return self.title
