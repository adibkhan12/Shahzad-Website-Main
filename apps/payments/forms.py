from django import forms

from apps.orders.models import Order


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=40)
    address_line1 = forms.CharField(max_length=255, label="Address")
    address_line2 = forms.CharField(max_length=255, required=False, label="Apt/Suite")
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=80, initial="UAE")
    payment_method = forms.ChoiceField(
        choices=Order.PaymentMethod.choices,
        initial=Order.PaymentMethod.COD,
        widget=forms.RadioSelect,
    )
    referral_source = forms.CharField(max_length=64, required=False)
    referral_other = forms.CharField(max_length=255, required=False)
