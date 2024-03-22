from django.urls import path

from alfa_romeo_web.checkout.views import ProfileEditView

urlpatterns = (
    path('first_step/<int:pk>/', ProfileEditView.as_view(), name='first_step'),
)