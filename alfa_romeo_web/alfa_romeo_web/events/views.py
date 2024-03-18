from django.views import generic as views

from alfa_romeo_web.events.models import Event


class ListEventsView(views.ListView):
    model = Event
    template_name = 'events/event_listing.html'
    paginate_by = 3

    def get_queryset(self):
        queryset = Event.objects.all().filter(is_active=True).order_by('-created')

        return queryset


class DetailEventView(views.DetailView):
    model = Event
    template_name = 'events/event_details.html'
