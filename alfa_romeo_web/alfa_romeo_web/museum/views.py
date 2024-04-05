from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
from alfa_romeo_web.museum.models import MuseumCategory, MuseumTopic


class MuseumCategoryView(views.ListView):
    model = MuseumCategory
    template_name = 'museum/museum_categories.html'

    def get_queryset(self):
        queryset = MuseumCategory.objects.filter(is_active=True)

        return queryset


class ListMuseumView(views.ListView):
    model = MuseumTopic
    paginate_by = 8
    template_name = 'museum/museum_listings.html'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        order_by = self.request.GET.get('order_by', 'year asc')

        if category_id:
            queryset = MuseumTopic.get_all_topics_by_categoryid(category_id).filter(is_active=True)
        else:
            queryset = MuseumTopic.objects.all()

        if order_by == 'header':
            queryset = queryset.order_by('header')
        elif order_by == 'year asc':
            queryset = queryset.order_by('year')
        elif order_by == 'year desc':
            queryset = queryset.order_by('-year')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = MuseumCategory.get_all_categories()
        for item in context['object_list']:
            if item.category:
                item.category_name = item.category.name.strip()
            else:
                item.category_name = None

        context['order_by'] = self.request.GET.get('order_by', 'year')

        context['category_id'] = self.request.GET.get('category')

        context['categories'] = categories
        return context


class DetailMuseumTopicView(views.DetailView):
    model = MuseumTopic
    template_name = 'museum/museum_topic_details.html'


class StaffMuseumTopicListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = MuseumTopic
    template_name = 'museum/staff_museum_topic.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = MuseumTopic.objects.all()
        order_by = self.request.GET.get('order_by', 'is_active')

        search_query = self.request.GET.get('Search')
        if search_query:
            initial_queryset = queryset.filter(
                Q(header__icontains=search_query)
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


class StaffMuseumTopicEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = MuseumTopic.objects.all()
    template_name = "museum/staff_edit_museum_topic.html"
    fields = ("header", "img_field", "description", "year", "category", "is_active", "slug")

    def get_success_url(self):
        return reverse('staff_museum')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class StaffMuseumTopicCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = MuseumTopic
    template_name = 'museum/staff_create_museum_topic.html'
    fields = ("header", "img_field", "description", "year", "category", "is_active", "slug")
    success_url = reverse_lazy('staff_museum')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class StaffMuseumTopicDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = MuseumTopic
    template_name = "museum/staff_delete_museum_topic.html"
    success_url = reverse_lazy('staff_museum')


class StaffMuseumCategoryListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = MuseumCategory
    template_name = 'museum/staff_museum_categories.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = MuseumCategory.objects.all()
        order_by = self.request.GET.get('order_by', 'is_active')

        search_query = self.request.GET.get('Search')
        if search_query:
            initial_queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        else:
            initial_queryset = queryset

        if order_by == 'is_active':
            queryset = initial_queryset.order_by('-is_active')
        elif order_by == 'not_active':
            queryset = initial_queryset.order_by('is_active')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_by'] = self.request.GET.get('order_by', 'is_active')
        context['search_query'] = self.request.GET.get('Search', '')

        return context


class StaffMuseumCategoryEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = MuseumCategory.objects.all()
    template_name = "museum/staff_edit_museum_category.html"
    fields = ("name", "img_field", "is_active")

    def get_success_url(self):
        return reverse('staff_museum_categories')


class StaffMuseumCategoryCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = MuseumCategory
    template_name = 'museum/staff_create_museum_category.html'
    fields = ("name", "img_field", "is_active")
    success_url = reverse_lazy('staff_museum_categories')


class StaffMuseumCategoryDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = MuseumCategory
    template_name = "museum/staff_delete_museum_category.html"
    success_url = reverse_lazy('staff_museum_categories')
