from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.forms import inlineformset_factory

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
from alfa_romeo_web.events.forms import EventForm, EventImageForm
from alfa_romeo_web.events.models import Event, EventImage


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

        search_query = self.request.GET.get('Search')
        if search_query:
            initial_queryset = queryset.filter(
                Q(title__icontains=search_query)
            )
        else:
            initial_queryset = queryset

        if order_by == 'is_active':
            queryset = initial_queryset.order_by('-is_active')
        if order_by == 'not_active':
            queryset = initial_queryset.order_by('is_active')
        elif order_by == 'created':
            queryset = initial_queryset.order_by('-created')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_by'] = self.request.GET.get('order_by', '-created')
        context['search_query'] = self.request.GET.get('Search', '')

        return context


class StaffEventEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = Event.objects.all()
    template_name = "events/staff_edit_event.html"
    form_class = EventForm  # Use your main event form

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        EventImageFormSet = inlineformset_factory(Event, EventImage, form=EventImageForm, extra=5, can_delete=True)
        if self.request.POST:
            data['image_formset'] = EventImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['image_formset'] = EventImageFormSet(instance=self.object)

        # data['existing_images'] = self.object.images.all()
        existing_images = self.object.images.all()
        max_num = 5  # Max number of images allowed

        if existing_images.count() >= max_num:
            # If the number of existing images is equal to or greater than the maximum allowed,
            # adjust the formset accordingly to prevent adding more images.
            data['image_formset'].extra = 0
        else:
            # Otherwise, limit the number of extra forms in the formset based on the remaining slots.
            remaining_slots = max_num - existing_images.count()
            data['image_formset'].extra = remaining_slots

        data['existing_images'] = existing_images
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('staff_event')


# class StaffEventEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
#     queryset = Event.objects.all()
#     template_name = "events/staff_edit_event.html"
#     fields = ("title", "description", "event_date", "location", "is_active", "slug")
#
#     def get_success_url(self):
#         return reverse('staff_event')
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)


# class StaffEventCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
#     model = Event
#     template_name = 'events/staff_create_event.html'
#     fields = ("title", "description", "event_date", "location", "is_active", "slug")
#     success_url = reverse_lazy('staff_event')
#
#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

# class StaffEventCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
#     model = Event
#     template_name = 'events/staff_create_event.html'
#     form_class = EventForm  # Use your main event form
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         EventImageFormSet = inlineformset_factory(Event, EventImage, form=EventImageForm, extra=5, can_delete=True)
#
#         if self.request.POST:
#             data['image_formset'] = EventImageFormSet(self.request.POST, self.request.FILES)
#         else:
#             data['image_formset'] = EventImageFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         image_formset = context['image_formset']
#         if image_formset.is_valid():
#             self.object = form.save()
#             image_formset.instance = self.object
#             image_formset.save()
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(self.get_context_data(form=form))
#
#     def get_success_url(self):
#         return reverse_lazy('staff_event')

class StaffEventCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = Event
    template_name = 'events/staff_create_event.html'
    form_class = EventForm

    def form_valid(self, form):
        images = self.request.FILES.getlist('images')
        if images:
            event = form.save(commit=False)
            event.created_by = self.request.user
            event.save()
            for image in images:
                EventImage.objects.create(event=event, image=image)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('staff_event')


class StaffEventDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = Event
    template_name = "events/staff_delete_event.html"
    success_url = reverse_lazy('staff_event')
