from django.urls import path, include

from alfa_romeo_web.history.views import HistoryCategoryView, StaffHistoryListView, \
    StaffHistoryCreateView, StaffHistoryEditView, StaffHistoryDeleteView, ListHistoryView

urlpatterns = (
    path('staff/', include([
        path('', StaffHistoryListView.as_view(), name='staff_history'),
        path('create_hisotry/', StaffHistoryCreateView.as_view(), name='staff_create_history'),
        path('edit_history/<int:pk>/', StaffHistoryEditView.as_view(), name='staff_edit_history'),
        path('delete_history/<int:pk>/', StaffHistoryDeleteView.as_view(), name='staff_delete_history'),
    ])),

    path('categories/', HistoryCategoryView.as_view(), name='history_categories'),
    path('details/', ListHistoryView.as_view(), name='history_list'),
)