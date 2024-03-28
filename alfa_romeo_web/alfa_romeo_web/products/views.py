from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
from alfa_romeo_web.products.models import Products, Category


class ListProductsView(views.ListView):
    model = Products
    paginate_by = 8
    template_name = 'products/products_list.html'

    def get_queryset(self):
        category_id = self.request.GET.get('category')
        order_by = self.request.GET.get('order_by', 'created')

        if category_id:
            queryset = Products.get_all_products_by_categoryid(category_id).filter(is_active=True)
        else:
            queryset = Products.get_all_products().filter(is_active=True)

        queryset = queryset.exclude(category__name="Tickets")

        if order_by == 'title':
            queryset = queryset.order_by('title')
        elif order_by == 'created':
            queryset = queryset.order_by('-created')
        elif order_by == 'price asc':
            queryset = queryset.order_by('price')
        elif order_by == 'price desc':
            queryset = queryset.order_by('-price')

        search_query = self.request.GET.get('Search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.get_all_categories()

        # Exclude the category "tickets"
        categories = [category for category in categories if category.name != "Tickets"]

        context['order_by'] = self.request.GET.get('order_by', 'created')
        context['search_query'] = self.request.GET.get('Search', '')
        context['category_id'] = self.request.GET.get('category')
        context['categories'] = categories

        return context


class ListTicketsView(views.ListView):
    model = Products
    paginate_by = 8
    template_name = 'products/tickets_list.html'

    def get_queryset(self):
        category = Category.objects.get(name='Tickets')
        if category:
            queryset = Products.get_all_products_by_categoryid(category.id).filter(is_active=True)
        else:
            queryset = Products.get_all_products().filter(is_active=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.get_all_categories()

        # Include only category "tickets"
        categories = [category for category in categories if category.name == "Tickets"]

        context['categories'] = categories
        return context


class DetailProductView(views.DetailView):
    model = Products
    template_name = 'products/product_details.html'


class ProductsStaffListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = Products
    template_name = 'products/staff_products.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = Products.objects.all()
        order_by = self.request.GET.get('order_by', 'is_active')

        if order_by == 'is_active':
            queryset = queryset.order_by('-is_active')
        if order_by == 'not_active':
            queryset = queryset.order_by('is_active')
        elif order_by == 'created':
            queryset = queryset.order_by('-created')
        elif order_by == 'category':
            queryset = queryset.order_by('category')

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


class StaffProductEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = Products.objects.all()
    template_name = "products/staff_edit_product.html"
    fields = ("title", "price", "discount_price", "category", "description", "image", "is_active", "slug")

    def get_success_url(self):
        return reverse('staff_products_list')


class StaffProductCreateView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.CreateView):
    model = Products
    template_name = 'products/staff_create_product.html'
    fields = ("title", "price", "discount_price", "category", "description", "image", "is_active", "slug")
    success_url = reverse_lazy('staff_products_list')


class StaffProductDeleteView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.DeleteView):
    model = Products
    template_name = "products/staff_delete_product.html"
    success_url = reverse_lazy('staff_products_list')

