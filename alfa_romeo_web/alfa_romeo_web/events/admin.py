from django.contrib import admin

from alfa_romeo_web.events.models import Event, EventImage


@admin.register(Event)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'is_active', 'pk', 'title', 'location', 'event_date', 'created', 'updated')
    ordering = ('pk',)
    search_fields = ('header',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_by',)
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(EventImage)
class ModelImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image',)
    ordering = ('event', 'image',)
