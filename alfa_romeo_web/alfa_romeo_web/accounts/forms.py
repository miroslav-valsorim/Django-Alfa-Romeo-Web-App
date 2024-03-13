from django.contrib.auth import get_user_model, forms as auth_forms

from alfa_romeo_web.accounts.models import AlfaRomeoUser

UserModel = get_user_model()


# class CreateUserForm(auth_forms.UserCreationForm):
#     class Meta:
#         model = UserModel
#         fields = ('username', 'email')

# from django.contrib.auth import forms as auth_forms, get_user_model
#
# UserModel = get_user_model()


class AlfaRomeoUserCreationForm(auth_forms.UserCreationForm):
    # user = None

    class Meta(auth_forms.UserCreationForm.Meta):
        model = AlfaRomeoUser
        fields = ('email',)


# class AlfaRomeoChangeForm(auth_forms.UserChangeForm):
#     class Meta(auth_forms.UserChangeForm.Meta):
#         model = UserModel
#
