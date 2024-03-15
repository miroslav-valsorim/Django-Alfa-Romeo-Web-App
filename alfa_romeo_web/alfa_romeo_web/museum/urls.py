from django.urls import path

from alfa_romeo_web.museum.views import MuseumCategoryView, ListMuseumView, DetailMuseumTopicView

urlpatterns = (
    path('categories/', MuseumCategoryView.as_view(), name="museum_categories"),
    path('gallery/', ListMuseumView.as_view(), name="museum_listing"),
    path('gallery/detail/<slug:slug>/', DetailMuseumTopicView.as_view(), name="museum_topic_detail")
)
