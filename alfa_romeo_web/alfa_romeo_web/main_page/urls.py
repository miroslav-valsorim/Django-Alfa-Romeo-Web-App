from django.urls import path

from alfa_romeo_web.main_page.views import MainListView

urlpatterns = (
    path("", MainListView.as_view(), name="main_page"),
)