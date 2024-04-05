from django import forms

from alfa_romeo_web.checkout.models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ['user',]
