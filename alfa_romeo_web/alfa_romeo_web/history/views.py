from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
from alfa_romeo_web.history.models import HistoryCategory, History


class HistoryCategoryView(views.ListView):
    model = HistoryCategory
    template_name = 'history/history_categories.html'

    def get_queryset(self):
        queryset = HistoryCategory.objects.filter(is_active=True)

        return queryset


class ListHistoryView(views.ListView):
    model = History
    template_name = 'history/history_details.html'

    def get_queryset(self):
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = History.get_all_stories_by_categoryid(category_id).filter(is_active=True)
        else:
            queryset = History.get_all_stories().filter(is_active=True)

        return queryset


class StaffHistoryListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = History
    template_name = 'history/staff_history.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = History.objects.all()
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


class StaffHistoryEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = History.objects.all()
    template_name = "history/staff_edit_history.html"
    fields = ("header", "img_field", "description", "category", "is_active")

    def get_success_url(self):
        return reverse('staff_history')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class StaffHistoryCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = History
    template_name = 'history/staff_create_history.html'
    fields = ("header", "img_field", "description", "category", "is_active")
    success_url = reverse_lazy('staff_history')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class StaffHistoryDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = History
    template_name = "history/staff_delete_history.html"
    success_url = reverse_lazy('staff_history')


class StaffHistoryCategoryListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = HistoryCategory
    template_name = 'history/staff_history_categories.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = HistoryCategory.objects.all()
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


class StaffHistoryCategoryEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = HistoryCategory.objects.all()
    template_name = "history/staff_edit_history_category.html"
    fields = ("name", "img_field", "is_active")

    def get_success_url(self):
        return reverse('staff_history_categories')


class StaffHistoryCategoryCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = HistoryCategory
    template_name = 'history/staff_create_history_category.html'
    fields = ("name", "img_field", "is_active")
    success_url = reverse_lazy('staff_history_categories')


class StaffHistoryCategoryDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = HistoryCategory
    template_name = "history/staff_delete_history_category.html"
    success_url = reverse_lazy('staff_history_categories')
