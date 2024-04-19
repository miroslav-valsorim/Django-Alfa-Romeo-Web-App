from django import forms
from django.utils.translation import gettext_lazy as _

from alfa_romeo_web.checkout.models import ShippingAddress


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ['user',]

        widgets = {
            'shipping_address': forms.TextInput(attrs={'placeholder': _('Enter your shipping address')}),
            'shipping_address_two': forms.TextInput(attrs={'placeholder': _('Enter your second shipping address')}),
            'country': forms.TextInput(attrs={'placeholder': _('Enter your country')}),
            'town': forms.TextInput(attrs={'placeholder': _('Enter your town')}),
            'zip': forms.TextInput(attrs={'placeholder': _('Enter your zip code')}),
        }
