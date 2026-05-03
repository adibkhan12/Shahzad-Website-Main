from django.conf import settings
from django.db import models


class Cart(models.Model):
    """One row per user or per anonymous session key."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    session_key = models.CharField(max_length=64, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # `condition=` replaces `check=` in Django 5.1+; the former is
            # removed in Django 6.0.
            models.CheckConstraint(
                condition=models.Q(user__isnull=False) | models.Q(session_key__isnull=False),
                name="cart_has_owner",
            ),
        ]

    @property
    def subtotal(self):
        return sum((i.line_total for i in self.items.all()), start=0)

    @property
    def count(self):
        return sum(i.quantity for i in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("cart", "product")]

    @property
    def line_total(self):
        # Use effective_price so cart subtotal, line_total, and downstream order
        # totals all honor an active sale_price. Previously used .price (regular)
        # which silently overcharged customers on sale items.
        return self.product.effective_price * self.quantity
