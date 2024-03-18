from django.views import generic as views

from alfa_romeo_web.events.models import Event


class MainListView(views.ListView):
    template_name = 'main_page/main.html'
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # limit the items up to 3 or 4 on the main page and show the newest (latest added)
        context['event_list'] = Event.objects.all().filter(is_active=True).order_by('-created')[:3]
        # context['news_list'] = News.objects.all()
        # context['merch'] = Merch.objects.all()
        return context
