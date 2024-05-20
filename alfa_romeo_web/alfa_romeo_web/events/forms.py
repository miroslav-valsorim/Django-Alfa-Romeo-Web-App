from django import forms
from django.core.exceptions import ValidationError

from .models import Event, EventImage
from multiupload.fields import MultiFileField


class EventForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1,
        max_num=5,
        max_file_size=1024 * 1024 * 5,  # 5MB
        required=False
    )

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

    def clean_image(self):
        image = self.cleaned_data.get('image')
        event = self.cleaned_data.get('event')

        if event and event.images.count() > 5:
            raise ValidationError("Cannot add more than 5 images to event.")

        return image


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "event_date", "location", "is_active", "slug")