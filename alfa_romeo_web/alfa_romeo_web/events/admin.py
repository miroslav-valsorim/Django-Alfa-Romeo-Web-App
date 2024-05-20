from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from alfa_romeo_web.events.forms import EventImageForm
from alfa_romeo_web.events.models import Event, EventImage


# class EventImageInline(admin.TabularInline):
#     model = EventImage
#     extra = 1

class EventImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Start with the current count of images associated with the product
        total_images_count = self.instance.images.count()

        # Calculate how many forms are marked for deletion
        to_delete = sum(1 for form in self.forms if form.cleaned_data.get('DELETE', False))

        # Calculate how many new images are being added (i.e., not marked for deletion)
        to_add = sum(1 for form in self.forms if not form.cleaned_data.get('DELETE', False) and not form.instance.pk)

        # Calculate the final count of images after considering deletions and additions
        final_count = total_images_count - to_delete + to_add

        if final_count > 5:
            raise ValidationError("Cannot have more than 5 images for a single event.")


class EventImageInline(admin.TabularInline):
    model = EventImage
    form = EventImageForm
    formset = EventImageInlineFormSet
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'is_active', 'pk', 'title', 'location', 'event_date', 'created', 'updated')
    ordering = ('pk',)
    search_fields = ('title',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_by',)
    list_per_page = 20
    inlines = [EventImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EventImage)
class ModelImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image',)
    ordering = ('event', 'image',)
