from django import forms
from .models import Event, EventImage


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "event_date", "location", "is_active", "slug")


class EventImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    )

    class Meta:
        model = EventImage
        fields = ('image',)
