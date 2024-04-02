from django.contrib import admin
from django.db.models import F

from alfa_romeo_web.history.models import HistoryCategory, History


@admin.register(HistoryCategory)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_active',)
    list_filter = ('is_active',)
    list_per_page = 20
    list_editable = ('is_active',)


@admin.register(History)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_category_name', 'created_by', 'is_active', 'id', 'header', 'created', 'updated')
    ordering = ('category__name', 'pk',)
    search_fields = ('header', 'category__name')
    search_help_text = 'Search by Header, Category'
    list_editable = ('is_active',)
    list_per_page = 20
    list_filter = ('is_active',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(category_name=F('category__name'))
        return queryset

    def get_category_name(self, obj):
        return obj.category.name

    get_category_name.short_description = 'Category Name'
    get_category_name.admin_order_field = 'category__name'
