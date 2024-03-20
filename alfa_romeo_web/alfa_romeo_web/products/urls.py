from django.urls import path

from alfa_romeo_web.products.views import ListProductsView, ListTicketsView, DetailProductView

urlpatterns = (
    path('', ListProductsView.as_view(), name='products_list'),
    path('tickets/', ListTicketsView.as_view(), name='tickets_list'),
    path('details/<slug:slug>/', DetailProductView.as_view(), name='product_details'),
)