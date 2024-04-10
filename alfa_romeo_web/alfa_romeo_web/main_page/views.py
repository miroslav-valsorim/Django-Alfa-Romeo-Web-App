from django.shortcuts import render
from django.views import generic as views

from alfa_romeo_web.events.models import Event
from alfa_romeo_web.news.models import News
from alfa_romeo_web.products.models import Products


class MainListView(views.ListView):
    template_name = 'main_page/main.html'
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # limit the items up to 3 or 4 on the main page and show the newest (latest added)
        context['event_list'] = Event.objects.all().filter(is_active=True).order_by('-created')[:3]
        context['news_list'] = News.objects.all().filter(is_active=True).order_by('-created')[:3]
        context['products_list'] = Products.objects.all().filter(is_active=True).exclude(category__name='Tickets').order_by('-created')[:3]
        return context


def custom_403(request, exception):
    return render(request, '403.html')
