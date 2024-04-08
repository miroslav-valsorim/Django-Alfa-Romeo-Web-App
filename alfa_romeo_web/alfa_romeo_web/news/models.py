from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class News(models.Model):
    MAX_TITLE_LENGTH = 150

    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='news_creator',
        default='Admin',
        null=True,
        blank=True,
    )

    title = models.CharField(
            max_length=150,
            blank=False,
            null=False,
        )

    # img_field = models.ImageField(
    #     upload_to='news/',
    #     blank=False,
    #     null=False,
    # )

    img_field = CloudinaryField(
        'image',
        blank=False,
        null=False,
    )

    description = models.TextField(
        blank=False,
        null=False,
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

    class Meta:
        verbose_name_plural = "News"
