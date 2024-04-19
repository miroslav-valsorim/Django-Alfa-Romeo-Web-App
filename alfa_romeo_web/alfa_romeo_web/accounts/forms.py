from django import forms
from django.contrib.auth import get_user_model, forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from alfa_romeo_web.accounts.models import AlfaRomeoUser

UserModel = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Your Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Your Password'


class AlfaRomeoUserCreationForm(auth_forms.UserCreationForm):
    # user = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = AlfaRomeoUser
        fields = ('email', 'password1', 'password2',)

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': _('Enter your email')}),
            'password1': forms.PasswordInput(attrs={'placeholder': _('Enter your password')}),
            'password2': forms.PasswordInput(attrs={'placeholder': _('Confirm your password')}),
        }
    # password1, password2 didn't work for some reason, so they are set in the HTML file (register_user.html)


# for admin panel
class AlfaRomeoChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
        fields = '__all__'

        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': _('Enter user email')}),
        }