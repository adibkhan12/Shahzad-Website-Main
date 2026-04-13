from django import forms

from .models import RepairBooking


class RepairBookingForm(forms.ModelForm):
    class Meta:
        model = RepairBooking
        fields = [
            "name", "email", "phone",
            "device_brand", "device_model",
            "issue", "preferred_drop_off",
        ]
        widgets = {
            "issue": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the issue (e.g. screen cracked, won't charge, water damage)…"}),
            "preferred_drop_off": forms.DateInput(attrs={"type": "date"}),
        }
