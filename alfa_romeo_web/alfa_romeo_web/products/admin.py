from django.contrib import admin
from django.db.models import F

from alfa_romeo_web.products.models import Category, Products


@admin.register(Category)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_active',)
    ordering = ('pk',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)


@admin.register(Products)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_category_name', 'is_active', 'title', 'created', 'updated')
    list_per_page = 20
    ordering = ('pk', 'category__name',)
    search_fields = ('title', 'category__name')
    search_help_text = 'Search by Title, Category'
    list_editable = ('is_active',)
    list_filter = ('is_active',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(category_name=F('category__name'))
        return queryset

    def get_category_name(self, obj):
        return obj.category.name

    get_category_name.short_description = 'Category Name'
    get_category_name.admin_order_field = 'category__name'
