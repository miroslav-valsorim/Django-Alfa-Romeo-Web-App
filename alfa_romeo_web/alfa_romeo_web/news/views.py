from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
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


class StaffNewsListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = News
    template_name = 'news/staff_news.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = News.objects.all()
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


class StaffNewsEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = News.objects.all()
    template_name = "news/staff_edit_news.html"
    fields = ("created_by", "title", "img_field", "description", "is_active", "img_field", "is_active", "slug")

    def get_success_url(self):
        return reverse('staff_news')


class StaffNewsCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = News
    template_name = 'news/staff_create_news.html'
    fields = ("created_by", "title", "img_field", "description", "is_active", "img_field", "is_active", "slug")
    success_url = reverse_lazy('staff_news')


class StaffNewsDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = News
    template_name = "news/staff_delete_news.html"
    success_url = reverse_lazy('staff_news')
