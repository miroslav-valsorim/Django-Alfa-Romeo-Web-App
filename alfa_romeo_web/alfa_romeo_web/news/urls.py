from django.urls import path, include

from alfa_romeo_web.news.views import DetailNewsView, StaffNewsListView, StaffNewsCreateView, \
    StaffNewsEditView, StaffNewsDeleteView, NewsList

urlpatterns = (
    path('staff/', include([
        path('', StaffNewsListView.as_view(), name='staff_news'),
        path('create_news/', StaffNewsCreateView.as_view(), name='staff_create_news'),
        path('edit_news/<slug:slug>/', StaffNewsEditView.as_view(), name='staff_edit_news'),
        path('delete_news/<slug:slug>/', StaffNewsDeleteView.as_view(), name='staff_delete_news'),

    ])),

    path('', NewsList.as_view(), name='news_list'),
    # path('', ListNewsView.as_view(), name='news_list'),
    path('details/<slug:slug>/', DetailNewsView.as_view(), name='news_details'),
)