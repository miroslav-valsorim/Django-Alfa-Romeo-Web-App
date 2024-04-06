from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class Event(models.Model):
    MAX_TITLE_LENGTH = 150
    MAX_LOCATION_LENGTH = 200

    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='event_creator',
        null=True,
        blank=True,
    )

    title = models.CharField(
            max_length=150,
            blank=False,
            null=False,
        )

    img_field = models.ImageField(
        upload_to='events/',
        blank=False,
        null=False,
    )

    description = models.TextField(
        blank=False,
        null=False,
    )

    event_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=MAX_LOCATION_LENGTH,
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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:  # slugify("My name") -> "My-name"
            self.slug = slugify(f"{self.title}-{self.pk}")

        super().save(*args, **kwargs)
