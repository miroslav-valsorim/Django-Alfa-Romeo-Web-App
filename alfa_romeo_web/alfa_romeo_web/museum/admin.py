from django.contrib import admin

from alfa_romeo_web.museum.models import MuseumCategory, MuseumTopic


@admin.register(MuseumCategory)
class ModelNameAdmin(admin.ModelAdmin):
    pass


@admin.register(MuseumTopic)
class ModelNameAdmin(admin.ModelAdmin):
    pass
