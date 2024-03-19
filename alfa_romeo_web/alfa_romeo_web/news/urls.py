from django.urls import path

from alfa_romeo_web.news.views import ListNewsView, DetailNewsView


urlpatterns = (
    path('', ListNewsView.as_view(), name='news_list'),
    path('details/<slug:slug>/', DetailNewsView.as_view(), name='news_details'),
)