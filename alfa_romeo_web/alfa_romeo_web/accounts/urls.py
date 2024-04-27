from django.urls import path, include
from django.contrib.auth import views as auth_views

from alfa_romeo_web.accounts.views import (LoginUserView, RegisterUserView, logout_view, ProfileDetailsView,
                                           ProfileEditView, ProfileDeleteView, ProfileChangePasswordView,
                                           StaffPanelView, ProfileOrdersView)

urlpatterns = (
    # Password Reset from django
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Our Urls
    path('staff_panel/', StaffPanelView.as_view(), name='staff_panel'),
    path("login/", LoginUserView.as_view(), name='login-user'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('logout/', logout_view, name='logout-user'),
    path(
        'profile/<int:pk>/',
        include([
            path("", ProfileDetailsView.as_view(), name="details-profile"),
            path("edit/", ProfileEditView.as_view(), name="edit-profile"),
            path("delete/", ProfileDeleteView.as_view(), name="delete-profile"),
            path("password/", ProfileChangePasswordView.as_view(), name="password-change"),
            path("orders/", ProfileOrdersView.as_view(), name="orders-profile")
        ]),
    )
)
