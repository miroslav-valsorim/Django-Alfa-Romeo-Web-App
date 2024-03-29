from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
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


class StaffEventListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = Event
    template_name = 'events/staff_event.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = Event.objects.all()
        order_by = self.request.GET.get('order_by', 'is_active')

        if order_by == 'is_active':
            queryset = queryset.order_by('-is_active')
        if order_by == 'not_active':
            queryset = queryset.order_by('is_active')
        elif order_by == 'created':
            queryset = queryset.order_by('-created')

        search_query = self.request.GET.get('Search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_by'] = self.request.GET.get('order_by', '-created')
        context['search_query'] = self.request.GET.get('Search', '')

        return context


class StaffEventEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = Event.objects.all()
    template_name = "events/staff_edit_event.html"
    fields = ("created_by", "title", "img_field", "description", "event_date", "location", "img_field", "is_active", "slug")

    def get_success_url(self):
        return reverse('staff_event')


class StaffEventCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = Event
    template_name = 'events/staff_create_event.html'
    fields = ("created_by", "title", "img_field", "description", "event_date", "location", "img_field", "is_active", "slug")
    success_url = reverse_lazy('staff_event')


class StaffEventDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = Event
    template_name = "events/staff_delete_event.html"
    success_url = reverse_lazy('staff_event')
