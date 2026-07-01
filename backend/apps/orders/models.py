import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        FAILED = "failed", "Failed"

    class PaymentMethod(models.TextChoices):
        COD = "cod", "Cash on delivery"
        CARD = "card", "Card / Apple Pay / Google Pay"
        TAMARA = "tamara", "Tamara"
        TABBY = "tabby", "Tabby"

    class Region(models.TextChoices):
        UAE = "UAE", "United Arab Emirates"
        KSA = "KSA", "Saudi Arabia"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )

    # billing / shipping snapshot
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=80, default="UAE")

    # region & money
    region = models.CharField(
        max_length=3,
        choices=Region.choices,
        default=Region.UAE,
        help_text="Determines shipping fee and which provider keys/URLs are used.",
    )
    currency = models.CharField(max_length=8, default="AED")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bnpl_surcharge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Legacy field. Always 0 — BNPL surcharge was removed.",
    )
    coupon_code = models.CharField(
        max_length=32,
        blank=True,
        help_text="Coupon code applied at checkout, if any.",
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="AED discount applied from coupon_code.",
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="subtotal + shipping_fee - discount_amount",
    )

    # payment
    payment_method = models.CharField(
        max_length=16, choices=PaymentMethod.choices, default=PaymentMethod.COD
    )
    provider = models.CharField(max_length=32, blank=True)
    provider_ref = models.CharField(max_length=128, blank=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)

    # attribution
    referral_source = models.CharField(max_length=64, blank=True)
    referral_other = models.CharField(max_length=255, blank=True)

    # stripe-shape copy for provider compatibility (optional)
    line_items = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.reference.hex[:8]}"

    @property
    def short_ref(self):
        return self.reference.hex[:8].upper()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.URLField(blank=True)

    @property
    def line_total(self):
        return self.unit_price * self.quantity
