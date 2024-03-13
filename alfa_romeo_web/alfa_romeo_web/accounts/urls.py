from django.urls import path, include

from alfa_romeo_web.accounts.views import (LoginUserView, RegisterUserView, logout_view, ProfileDetailsView,
                                           ProfileEditView, ProfileDeleteView, ProfileChangePasswordView)

urlpatterns = (
    path("login/", LoginUserView.as_view(), name='login-user'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('logout/', logout_view, name='logout-user'),
    path(
        'profile/<int:pk>/',
        include([
            path("", ProfileDetailsView.as_view(), name="details-profile"),
            path("edit/", ProfileEditView.as_view(), name="edit-profile"),
            path("delete/", ProfileDeleteView.as_view(), name="delete-profile"),
            path("password/", ProfileChangePasswordView.as_view(), name="password-change")
        ]),
    )
)
