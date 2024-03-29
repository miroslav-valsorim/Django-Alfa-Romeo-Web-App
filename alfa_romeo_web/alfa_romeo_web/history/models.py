from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class HistoryCategory(models.Model):
    name = models.CharField(max_length=50)
    img_field = models.ImageField(
        upload_to='history/',
        blank=False,
        null=False,
    )

    @staticmethod
    def get_all_categories():
        return HistoryCategory.objects.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "History Categories"


class History(models.Model):
    MAX_HEADER_LENGTH = 150

    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='history_creator',
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
    category = models.ForeignKey(
        HistoryCategory,
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

    class Meta:
        verbose_name_plural = "History"

    @staticmethod
    def get_story_by_id(ids):
        return History.objects.filter(id__in=ids)

    @staticmethod
    def get_all_stories():
        return History.objects.all()

    @staticmethod
    def get_all_stories_by_categoryid(category_id):
        if category_id:
            return History.objects.filter(category=category_id)
        else:
            return History.get_all_stories()

    def __str__(self):
        return f"ID: {self.id} / Category: {self.category} / Header: {self.header}"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     if not self.slug:  # slugify("My name") -> "My-name"
    #         self.slug = slugify(f"{self.category}-{self.header}-{self.pk}")
    #
    #     super().save(*args, **kwargs)
