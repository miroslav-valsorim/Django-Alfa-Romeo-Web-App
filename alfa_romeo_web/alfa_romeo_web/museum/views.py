from django.shortcuts import render
from django.views import generic as views

from alfa_romeo_web.museum.models import MuseumCategory, MuseumTopic


class MuseumCategoryView(views.ListView):
    model = MuseumCategory
    template_name = 'museum/museum_categories.html'


class ListGalleryView(views.ListView):
    model = MuseumTopic
    paginate_by = 2
    template_name = 'museum/museum_gallery.html'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        # if category_id:
        #     queryset = MuseumTopic.get_all_topics_by_categoryid(category_id)
        # else:
        #     queryset = MuseumTopic.get_all_topics()
        queryset = MuseumTopic.get_all_topics_by_categoryid(category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = MuseumCategory.get_all_categories()
        for item in context['object_list']:
            # Assuming MuseumCategory has a 'name' attribute representing the category name
            if item.category:
                item.category_name = item.category.name.strip()
            else:
                item.category_name = None

        context['categories'] = categories
        return context
