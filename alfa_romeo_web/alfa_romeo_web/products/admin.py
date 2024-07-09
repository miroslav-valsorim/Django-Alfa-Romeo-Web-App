# from django.contrib import admin
# from django.core.exceptions import ValidationError
# from django.db.models import F
# from django.forms import BaseInlineFormSet
#
# from alfa_romeo_web.products.forms import ProductImageForm
# from alfa_romeo_web.products.models import Category, Products, ProductImage
#
#
# @admin.register(Category)
# class ModelNameAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'is_active',)
#     ordering = ('pk',)
#     list_editable = ('is_active',)
#     list_filter = ('is_active',)
#
#
# class ProductImageInlineFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#
#         # Start with the current count of images associated with the product
#         total_images_count = self.instance.images.count()
#
#         # Calculate how many forms are marked for deletion
#         to_delete = sum(1 for form in self.forms if form.cleaned_data.get('DELETE', False))
#
#         # Calculate how many new images are being added (i.e., not marked for deletion)
#         to_add = sum(1 for form in self.forms if not form.cleaned_data.get('DELETE', False) and not form.instance.pk)
#
#         # Calculate the final count of images after considering deletions and additions
#         final_count = total_images_count - to_delete + to_add
#
#         if final_count > 5:
#             raise ValidationError("Cannot have more than 5 images for a single product.")
#
#
# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     form = ProductImageForm
#     formset = ProductImageInlineFormSet
#     extra = 1
#
#
# @admin.register(Products)
# class ModelNameAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'get_category_name', 'is_active', 'title', 'created', 'updated')
#     list_per_page = 20
#     ordering = ('pk', 'category__name',)
#     search_fields = ('title', 'category__name')
#     search_help_text = 'Search by Title, Category'
#     list_editable = ('is_active',)
#     list_filter = ('is_active',)
#     inlines = [ProductImageInline]
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(category_name=F('category__name'))
#         return queryset
#
#     def get_category_name(self, obj):
#         return obj.category.name
#
#     get_category_name.short_description = 'Category Name'
#     get_category_name.admin_order_field = 'category__name'
#
#
# @admin.register(ProductImage)
# class ModelImageAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image', )
#     ordering = ('product', 'image',)

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import F
from django.forms import BaseInlineFormSet

from alfa_romeo_web.products.forms import ProductImageForm
from alfa_romeo_web.products.models import Category, Products, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_active',)
    ordering = ('pk',)
    list_editable = ('is_active',)
    list_filter = ('is_active',)


class ProductImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if self.instance.pk is None:
            return  # Skip validation if the parent instance is not saved yet

        total_images_count = self.instance.images.count()
        to_delete = sum(1 for form in self.forms if form.cleaned_data.get('DELETE', False))
        to_add = sum(1 for form in self.forms if not form.cleaned_data.get('DELETE', False) and not form.instance.pk)
        final_count = total_images_count - to_delete + to_add

        if final_count > 5:
            raise ValidationError("Cannot have more than 5 images for a single product.")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    form = ProductImageForm
    formset = ProductImageInlineFormSet
    extra = 1


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_category_name', 'is_active', 'title', 'created', 'updated')
    list_per_page = 20
    ordering = ('pk', 'category__name',)
    search_fields = ('title', 'category__name')
    search_help_text = 'Search by Title, Category'
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    inlines = [ProductImageInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(category_name=F('category__name'))
        return queryset

    def get_category_name(self, obj):
        return obj.category.name

    get_category_name.short_description = 'Category Name'
    get_category_name.admin_order_field = 'category__name'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.save()  # Save the product to get a primary key before saving inline formsets
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        form.instance = form.save(commit=False)
        if not form.instance.pk:
            form.instance.save()  # Ensure the parent instance is saved before saving related objects
        super().save_related(request, form, formsets, change)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', )
    ordering = ('product', 'image',)
