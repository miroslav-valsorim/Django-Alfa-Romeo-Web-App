from django.urls import path, include

from alfa_romeo_web.museum.views import MuseumCategoryView, ListMuseumView, DetailMuseumTopicView, \
    StaffMuseumTopicListView, StaffMuseumTopicCreateView, StaffMuseumTopicEditView, StaffMuseumTopicDeleteView, \
    StaffMuseumCategoryListView, StaffMuseumCategoryCreateView, StaffMuseumCategoryEditView, \
    StaffMuseumCategoryDeleteView

urlpatterns = (
    path('staff/', include([
        path('', StaffMuseumTopicListView.as_view(), name='staff_museum'),
        path('create_museum_topic/', StaffMuseumTopicCreateView.as_view(), name='staff_create_museum_topic'),
        path('edit_museum_topic/<int:pk>/', StaffMuseumTopicEditView.as_view(), name='staff_edit_museum_topic'),
        path('delete_museum_topic/<int:pk>/', StaffMuseumTopicDeleteView.as_view(), name='staff_delete_museum_topic'),
        path('categories/', StaffMuseumCategoryListView.as_view(), name='staff_museum_categories'),
        path('create_museum_category/', StaffMuseumCategoryCreateView.as_view(), name='staff_create_museum_category'),
        path('edit_museum_category/<int:pk>/', StaffMuseumCategoryEditView.as_view(), name='staff_edit_museum_category'),
        path('delete_museum_category/<int:pk>/', StaffMuseumCategoryDeleteView.as_view(), name='staff_delete_museum_category'),
    ])),

    path('categories/', MuseumCategoryView.as_view(), name="museum_categories"),
    path('gallery/', ListMuseumView.as_view(), name="museum_listing"),
    path('gallery/detail/<slug:slug>/', DetailMuseumTopicView.as_view(), name="museum_topic_detail")
)
