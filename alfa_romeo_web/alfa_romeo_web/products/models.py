from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


class Category(models.Model):
    MAX_NAME_LENGTH = 50

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Products(models.Model):
    MAX_TITLE_LENGTH = 100
    MAX_DESCRIPTION_LENGTH = 250

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        blank=False,
        null=False,
        )

    quantity = models.IntegerField(
        default=0,
        blank=False,
        null=False,
    )

    price = models.IntegerField(
        default=0,
        blank=False,
        null=False,
    )

    discount_price = models.IntegerField(
        default=0,
        blank=True,
        null=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        )

    description = models.CharField(
        max_length=MAX_DESCRIPTION_LENGTH,
        blank=True,
        null=True,
    )

    # image = models.ImageField(
    #     upload_to='products/',
    #     blank=True,
    #     null=True,
    # )
    image = CloudinaryField(
        'image',
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Products"

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:  # slugify("My name") -> "My-name"
            self.slug = slugify(f"{self.category}-{self.title}-{self.pk}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title