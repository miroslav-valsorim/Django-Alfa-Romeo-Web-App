from django.contrib import admin

from alfa_romeo_web.forum.models import ForumCategory, Post, Comment, Reply


@admin.register(ForumCategory)
class ModelNameAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class ModelNameAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class ModelNameAdmin(admin.ModelAdmin):
    pass


@admin.register(Reply)
class ModelNameAdmin(admin.ModelAdmin):
    pass
