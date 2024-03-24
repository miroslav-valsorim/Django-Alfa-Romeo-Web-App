from django import forms

from alfa_romeo_web.accounts.models import Profile
from alfa_romeo_web.forum.models import Post, Comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories"]


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
