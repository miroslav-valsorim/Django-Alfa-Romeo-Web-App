from django.urls import path, include

from alfa_romeo_web.history.views import HistoryCategoryView, StaffHistoryListView, \
    StaffHistoryCreateView, StaffHistoryEditView, StaffHistoryDeleteView, ListHistoryView, StaffHistoryCategoryListView, \
    StaffHistoryCategoryDeleteView, StaffHistoryCategoryEditView, StaffHistoryCategoryCreateView

urlpatterns = (
    path('staff/', include([
        path('', StaffHistoryListView.as_view(), name='staff_history'),
        path('create_hisotry/', StaffHistoryCreateView.as_view(), name='staff_create_history'),
        path('edit_history/<int:pk>/', StaffHistoryEditView.as_view(), name='staff_edit_history'),
        path('delete_history/<int:pk>/', StaffHistoryDeleteView.as_view(), name='staff_delete_history'),
        path('categories/', StaffHistoryCategoryListView.as_view(), name='staff_history_categories'),
        path('create_hisotry_category/', StaffHistoryCategoryCreateView.as_view(), name='staff_create_history_category'),
        path('edit_history_category/<int:pk>/', StaffHistoryCategoryEditView.as_view(), name='staff_edit_history_category'),
        path('delete_history_category/<int:pk>/', StaffHistoryCategoryDeleteView.as_view(), name='staff_delete_history_category'),
    ])),

    path('categories/', HistoryCategoryView.as_view(), name='history_categories'),
    path('details/', ListHistoryView.as_view(), name='history_list'),
)