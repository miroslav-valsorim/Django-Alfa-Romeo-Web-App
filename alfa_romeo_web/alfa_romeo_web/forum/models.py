from django.db import models
from django.utils.text import slugify

from alfa_romeo_web.accounts.models import Profile


class ForumCategory(models.Model):
    MAX_TITLE_LENGTH = 50

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        blank=False,
        null=False,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    description = models.TextField(
        default="description",
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(ForumCategory, self).save(*args, **kwargs)

    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).filter(approved=True).count()

    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")


class Comment(models.Model):
    MAX_CONTENT_LENGTH = 400

    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        max_length=MAX_CONTENT_LENGTH,
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.content[:100]


class Post(models.Model):
    MAX_TITLE_LENGTH = 200
    MAX_CONTENT_LENGTH = 400

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        blank=False,
        null=False,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,

    )

    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    content = models.TextField(
        max_length=MAX_CONTENT_LENGTH,
        blank=False,
        null=False,
    )

    categories = models.ManyToManyField(
        ForumCategory,
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    approved = models.BooleanField(
        default=False,
    )

    comments = models.ManyToManyField(
        Comment,
        blank=True,
    )

    closed = models.BooleanField(
        default=False,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def num_comments(self):
        return self.comments.count()
