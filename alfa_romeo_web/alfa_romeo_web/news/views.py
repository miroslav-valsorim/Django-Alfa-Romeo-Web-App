from django.views import generic as views

from alfa_romeo_web.news.models import News


class ListNewsView(views.ListView):
    model = News
    template_name = 'news/news_listing.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = News.objects.all().filter(is_active=True).order_by('-created')

        return queryset


class DetailNewsView(views.DetailView):
    model = News
    template_name = 'news/news_details.html'
