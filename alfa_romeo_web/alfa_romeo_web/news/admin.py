from django.contrib import admin

from alfa_romeo_web.news.models import News


@admin.register(News)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_by', 'is_active', 'pk', 'title', 'created', 'updated')
    ordering = ('pk',)
    search_fields = ('header',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_by',)
    list_per_page = 20
