from django.urls import path

from alfa_romeo_web.cart.views import add_to_cart, remove_from_cart, ShoppingCartSummary, remove_single_item_from_cart, \
    add_single_item_to_cart

urlpatterns = (
    path('add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug:slug>/', remove_from_cart, name='remove_from_cart'),
    path('cart_details/', ShoppingCartSummary.as_view(), name='cart_details'),
    path('remove_item_from_cart/<slug:slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('add_item_to_cart/<slug:slug>/', add_single_item_to_cart, name='add_single_item_to_cart'),
)