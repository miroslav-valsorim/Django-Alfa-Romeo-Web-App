from django.shortcuts import render
from django.views import generic as views

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

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.get_all_categories()

        # Exclude the category "tickets"
        categories = [category for category in categories if category.name != "Tickets"]

        context['order_by'] = self.request.GET.get('order_by', 'created')

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
