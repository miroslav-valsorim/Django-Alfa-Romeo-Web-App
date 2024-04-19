from django import forms
from django.utils.translation import gettext_lazy as _

from alfa_romeo_web.accounts.models import Profile
from alfa_romeo_web.forum.models import Post


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': _('Enter your First Name')}),
            'last_name': forms.TextInput(attrs={'placeholder': _('Enter your Last Name')}),
        }


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories"]

