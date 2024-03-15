from django.urls import path

from alfa_romeo_web.museum.views import MuseumCategoryView, ListGalleryView

urlpatterns = (
    path('categories/', MuseumCategoryView.as_view(), name="museum_categories"),
    path('gallery/', ListGalleryView.as_view(), name="museum_gallery"),
)