from django.urls import path

from alfa_romeo_web.history.views import HistoryCategoryView, DetailHistoryView

urlpatterns = (
    path('categories/', HistoryCategoryView.as_view(), name='history_categories'),
    path('detail/<pk>/', DetailHistoryView.as_view(), name="history_details"),
)