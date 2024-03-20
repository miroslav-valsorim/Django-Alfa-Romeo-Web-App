from django.contrib import admin
from django.db.models import F

from alfa_romeo_web.products.models import Category, Products


@admin.register(Category)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


@admin.register(Products)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('get_category_name', 'id', 'is_active', 'title', 'created', 'updated')
    ordering = ('category__name',)
    search_fields = ('title', 'category__name')
    list_editable = ('is_active',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(category_name=F('category__name'))
        return queryset

    def get_category_name(self, obj):
        return obj.category.name

    get_category_name.short_description = 'Category Name'
    get_category_name.admin_order_field = 'category__name'
