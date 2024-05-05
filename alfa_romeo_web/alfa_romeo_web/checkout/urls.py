from django.urls import path, include

from alfa_romeo_web.checkout.views import ProfileEditView, CheckoutView, PaymentView, paypal_payment_successful, \
    paypal_payment_failed, StaffAddressListView, StaffAddressEditView

urlpatterns = (
    path('staff/', include([
        path('', StaffAddressListView.as_view(), name='staff_address_list'),
        path('edit_event/<int:pk>/', StaffAddressEditView.as_view(), name='staff_edit_address'),
    ])),

    path('first_step/<int:pk>/', ProfileEditView.as_view(), name='first_step'),
    path('second_step/<int:pk>/', CheckoutView.as_view(), name='second_step'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/success/<int:shopping_cart_id>/', paypal_payment_successful, name='paypal_payment_successful'),
    path('payment/failed/<int:shopping_cart_id>/', paypal_payment_failed, name='paypal_payment_failed'),

)