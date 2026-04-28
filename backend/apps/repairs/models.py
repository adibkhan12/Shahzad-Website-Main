import uuid

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class RepairService(models.Model):
    class Device(models.TextChoices):
        PHONE = "phone", "Mobile phone"
        LAPTOP = "laptop", "Laptop"
        TABLET = "tablet", "Tablet"
        WATCH = "watch", "Smart watch"
        OTHER = "other", "Other"

    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    device = models.CharField(max_length=12, choices=Device.choices, default=Device.PHONE)
    short_desc = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    est_minutes = models.PositiveIntegerField(default=30, help_text="Typical turnaround in minutes")
    icon = models.CharField(max_length=12, default="🔧", help_text="Emoji shown on cards")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("repairs:book", args=[self.slug])

    def __str__(self):
        return self.name


class RepairBooking(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        QUOTED = "quoted", "Quoted"
        IN_PROGRESS = "in_progress", "In progress"
        READY = "ready", "Ready for pickup"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    service = models.ForeignKey(
        RepairService, null=True, on_delete=models.SET_NULL, related_name="bookings"
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    device_brand = models.CharField(max_length=80)
    device_model = models.CharField(max_length=120)
    issue = models.TextField()
    preferred_drop_off = models.DateField(null=True, blank=True)
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Booking {self.reference.hex[:8]} — {self.device_model}"

    @property
    def short_ref(self):
        return self.reference.hex[:8].upper()
