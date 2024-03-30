from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class MuseumCategory(models.Model):
    MAX_CATEGORY_NAME_LENGTH = 50

    name = models.CharField(
        max_length=MAX_CATEGORY_NAME_LENGTH,
        blank=False,
        null=False,
    )

    img_field = models.ImageField(
        upload_to='museum_gallery/',
        blank=False,
        null=False,
    )

    is_active = models.BooleanField(
        default=True
    )

    @staticmethod
    def get_all_categories():
        return MuseumCategory.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Museum Categories"


class MuseumTopic(models.Model):
    MAX_HEADER_LENGTH = 150

    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='topic_creator',
    )
    header = models.CharField(
        max_length=MAX_HEADER_LENGTH,
        blank=False,
        null=False,
    )
    img_field = models.ImageField(
        upload_to='museum_gallery/',
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=False,
        null=False,
    )
    year = models.IntegerField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        MuseumCategory,
        on_delete=models.CASCADE,
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
        verbose_name_plural = "Museum Topics"

    @staticmethod
    def get_topics_by_id(ids):
        return MuseumTopic.objects.filter(id__in=ids)

    @staticmethod
    def get_all_topics():
        return MuseumTopic.objects.all()

    @staticmethod
    def get_all_topics_by_categoryid(category_id):
        if category_id:
            return MuseumTopic.objects.filter(category=category_id)
        else:
            return MuseumTopic.get_all_topics()

    def __str__(self):
        return f"ID: {self.id} / Category: {self.category} / Header: {self.header}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:  # slugify("My name") -> "My-name"
            self.slug = slugify(f"{self.category}-{self.header}-{self.pk}")

        super().save(*args, **kwargs)
