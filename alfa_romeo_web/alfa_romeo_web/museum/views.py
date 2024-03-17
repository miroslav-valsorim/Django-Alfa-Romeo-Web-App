from django.views import generic as views

from alfa_romeo_web.museum.models import MuseumCategory, MuseumTopic


class MuseumCategoryView(views.ListView):
    model = MuseumCategory
    template_name = 'museum/museum_categories.html'


class ListMuseumView(views.ListView):
    model = MuseumTopic
    paginate_by = 8
    template_name = 'museum/museum_listings.html'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        order_by = self.request.GET.get('order_by', 'year')

        if category_id:
            queryset = MuseumTopic.get_all_topics_by_categoryid(category_id).filter(is_active=True)
        else:
            queryset = MuseumTopic.objects.all()

        if order_by == 'header':
            queryset = queryset.order_by('header')
        else:
            queryset = queryset.order_by('year')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = MuseumCategory.get_all_categories()
        for item in context['object_list']:
            if item.category:
                item.category_name = item.category.name.strip()
            else:
                item.category_name = None

        context['order_by'] = self.request.GET.get('order_by', 'contributors')

        context['category_id'] = self.request.GET.get('category')

        context['categories'] = categories
        return context


class DetailMuseumTopicView(views.DetailView):
    model = MuseumTopic
    template_name = 'museum/museum_topic_details.html'
