from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percentage off"
        FIXED = "fixed", "Fixed amount off (AED)"

    class RegionScope(models.TextChoices):
        BOTH = "BOTH", "Both UAE & KSA"
        UAE = "UAE", "UAE only"
        KSA = "KSA", "KSA only"

    code = models.CharField(
        max_length=32,
        unique=True,
        help_text="Customer types this at checkout. Case-insensitive. e.g. WELCOME10",
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        help_text="Internal note — not shown to customers.",
    )

    discount_type = models.CharField(
        max_length=16, choices=DiscountType.choices, default=DiscountType.PERCENT
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="For 'percent': enter 10 for 10%. For 'fixed': enter 50 for AED 50 off.",
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional cap on percent discounts. Leave blank for no cap.",
    )

    min_subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Cart subtotal must be at least this much. 0 = no minimum.",
    )

    region_scope = models.CharField(
        max_length=4, choices=RegionScope.choices, default=RegionScope.BOTH
    )

    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Max total uses across all customers. Leave blank for unlimited.",
    )
    used_count = models.PositiveIntegerField(default=0, editable=False)
    per_user_limit = models.PositiveIntegerField(
        default=1,
        help_text="Max times one logged-in customer can use this code. 0 = unlimited.",
    )

    applies_to_categories = models.ManyToManyField(
        "catalog.Category",
        blank=True,
        related_name="coupons",
        help_text="Restrict to these categories. Leave empty to apply to all.",
    )
    applies_to_brands = models.ManyToManyField(
        "catalog.Brand",
        blank=True,
        related_name="coupons",
        help_text="Restrict to these brands. Leave empty to apply to all.",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    # ------------- validation & discount math -------------

    def validate_for(self, *, subtotal: Decimal, region: str, user=None, cart_items=None):
        """
        Returns (ok, message). cart_items: iterable of objects with .product
        (catalog.Product) — used to enforce category/brand restrictions.
        """
        if not self.is_active:
            return False, "This coupon is not active."

        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return False, "This coupon isn't valid yet."
        if self.valid_until and now > self.valid_until:
            return False, "This coupon has expired."

        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False, "This coupon has reached its usage limit."

        if user is not None and getattr(user, "is_authenticated", False) and self.per_user_limit:
            used = CouponRedemption.objects.filter(coupon=self, user=user).count()
            if used >= self.per_user_limit:
                return False, "You've already used this coupon."

        if self.region_scope != self.RegionScope.BOTH and region != self.region_scope:
            return False, f"This coupon is only valid for {self.region_scope} orders."

        if subtotal < self.min_subtotal:
            return (
                False,
                f"Add AED {(self.min_subtotal - subtotal):.2f} more to use this coupon "
                f"(minimum AED {self.min_subtotal:.0f}).",
            )

        # Category / brand restriction — at least one cart line must qualify.
        cat_ids = set(self.applies_to_categories.values_list("id", flat=True))
        brand_ids = set(self.applies_to_brands.values_list("id", flat=True))
        if (cat_ids or brand_ids) and cart_items is not None:
            ok_line = False
            for ci in cart_items:
                p = getattr(ci, "product", None)
                if p is None:
                    continue
                if cat_ids and p.category_id in cat_ids:
                    ok_line = True
                    break
                if brand_ids and p.brand_id in brand_ids:
                    ok_line = True
                    break
            if not ok_line:
                return False, "This coupon doesn't apply to the items in your cart."

        return True, "OK"

    def compute_discount(self, subtotal: Decimal) -> Decimal:
        """Caller is responsible for calling validate_for() first."""
        if self.discount_type == self.DiscountType.PERCENT:
            raw = (subtotal * self.discount_value / Decimal("100")).quantize(Decimal("0.01"))
        else:
            raw = self.discount_value
        if self.max_discount is not None:
            raw = min(raw, self.max_discount)
        # Never discount more than the subtotal itself.
        return min(raw, subtotal)


class CouponRedemption(models.Model):
    """One row per successful checkout that used a coupon. Used for per-user limits
    and historical reporting in the admin."""

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="redemptions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="coupon_redemptions",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="coupon_redemptions",
    )
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
