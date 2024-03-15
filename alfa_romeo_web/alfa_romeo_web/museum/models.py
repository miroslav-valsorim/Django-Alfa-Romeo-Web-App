from django.db import models
from django.utils.text import slugify


class MuseumCategory(models.Model):
    name = models.CharField(max_length=50)
    img_field = models.ImageField(
        upload_to='museum_gallery/',
        blank=False,
        null=False,
    )

    @staticmethod
    def get_all_categories():
        return MuseumCategory.objects.all()

    def __str__(self):
        return self.name


class MuseumTopic(models.Model):
    MAX_HEADER_LENGTH = 150
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
    category = models.ForeignKey(
        MuseumCategory,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
    )

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:  # slugify("My name") -> "My-name"
            self.slug = slugify(f"{self.category}-{self.header}-{self.pk}")

        super().save(*args, **kwargs)