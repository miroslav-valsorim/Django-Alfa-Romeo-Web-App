from django.urls import path

from alfa_romeo_web.checkout.views import ProfileEditView, CheckoutView, PaymentView, paypal_payment_successful, \
    paypal_payment_failed

urlpatterns = (
    path('first_step/<int:pk>/', ProfileEditView.as_view(), name='first_step'),
    path('second_step/<int:pk>/', CheckoutView.as_view(), name='second_step'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/success/<int:shopping_cart_id>/', paypal_payment_successful, name='paypal_payment_successful'),
    path('payment/failed/<int:shopping_cart_id>/', paypal_payment_failed, name='paypal_payment_failed'),

)