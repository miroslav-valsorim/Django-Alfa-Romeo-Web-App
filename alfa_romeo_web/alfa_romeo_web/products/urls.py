from django.urls import path, include

from alfa_romeo_web.products.views import ListProductsView, ListTicketsView, DetailProductView, ProductsStaffListView, \
    StaffProductEditView, StaffProductCreateView, StaffProductDeleteView

urlpatterns = (
    path('staff/', include([
        path('', ProductsStaffListView.as_view(), name='staff_products_list'),
        path('create_product/',StaffProductCreateView.as_view(), name='staff_create_product'),
        path('edit_product/<slug:slug>/', StaffProductEditView.as_view(), name='staff_edit_product'),
        path('delete_product/<slug:slug>/', StaffProductDeleteView.as_view(), name='staff_delete_product'),
    ])),

    path('', ListProductsView.as_view(), name='products_list'),
    path('tickets/', ListTicketsView.as_view(), name='tickets_list'),
    path('details/<slug:slug>/', DetailProductView.as_view(), name='product_details'),

)