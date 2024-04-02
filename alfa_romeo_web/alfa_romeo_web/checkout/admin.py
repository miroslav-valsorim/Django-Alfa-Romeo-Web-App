from django.contrib import admin

from alfa_romeo_web.checkout.models import ShippingAddress


@admin.register(ShippingAddress)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', )
    list_per_page = 20

