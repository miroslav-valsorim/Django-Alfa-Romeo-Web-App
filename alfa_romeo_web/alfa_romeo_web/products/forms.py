from django import forms
from django.core.exceptions import ValidationError

from .models import Products, ProductImage
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1,
        max_num=5,
        max_file_size=1024 * 1024 * 5,  # 5MB
        required=False
    )

    class Meta:
        model = Products
        fields = ("title", "price", "discount_price", "quantity", "category", "description", "is_active", "slug")


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    )

    class Meta:
        model = ProductImage
        fields = ("image", )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        product = self.cleaned_data.get('product')

        if product and product.images.count() > 5:
            raise ValidationError("Cannot add more than 5 images to a single product.")

        return image


class EditProductForm(forms.ModelForm):

    class Meta:
        model = Products
        fields = ("title", "price", "discount_price", "quantity", "category", "description", "is_active", "slug")