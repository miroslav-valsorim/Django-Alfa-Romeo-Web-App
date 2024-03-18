from django.contrib import admin

from alfa_romeo_web.events.models import Event


@admin.register(Event)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'is_active', 'pk', 'title', 'location', 'event_date', 'created', 'updated')
    ordering = ('pk',)
    search_fields = ('header',)
    list_editable = ('is_active',)
