from django.urls import path

from alfa_romeo_web.news.views import ListAPINewsView

urlpatterns = (
    path('', ListAPINewsView.as_view(), name='news_api_list'),
)