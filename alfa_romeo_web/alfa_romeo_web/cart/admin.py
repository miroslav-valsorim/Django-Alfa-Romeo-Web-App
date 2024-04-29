from django.contrib import admin

from alfa_romeo_web.cart.models import OrderItem, ShoppingCart


@admin.register(OrderItem)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user', 'quantity', 'ordered')
    search_fields = ('user',)
    search_help_text = 'Search by User'
    list_per_page = 20


@admin.register(ShoppingCart)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered', 'status')
    search_fields = ('user',)
    search_help_text = 'Search by User'
    list_per_page = 20
    list_filter = ('ordered',)