from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins as auth_mixins
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic as views

from alfa_romeo_web.accounts.mixin import CheckAdminOrStaffAccess
from alfa_romeo_web.cart.models import ShoppingCart, OrderItem
from alfa_romeo_web.checkout.models import ShippingAddress
from alfa_romeo_web.products.models import Products


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)

    if item.quantity <= 0:
        messages.error(request, "This item is out of stock.")
        return redirect("product_details", slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = ShoppingCart.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            item.quantity -= 1  # Reduce available quantity when added to cart
            item.save()
            messages.info(request, "This item quantity was updated")

        else:
            order.items.add(order_item)
            item.quantity -= 1  # Reduce available quantity when added to cart
            item.save()
            messages.info(request, "This item was added to your cart")
    else:
        ordered_date = timezone.now()
        order = ShoppingCart.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        item.quantity -= 1  # Reduce available quantity when added to cart
        item.save()
        messages.info(request, "This item was added to your cart")

    # return redirect("product_details", slug=slug)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)

    order_qs = ShoppingCart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_items = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )
            total_quantity_removed = 0
            for order_item in order_items:
                total_quantity_removed += order_item.quantity
                order.items.remove(order_item)
                order_item.delete()
            item.quantity += total_quantity_removed  # Increase available quantity
            item.save()
            messages.info(request, "This item was removed from your cart")
        else:
            messages.info(request, "This item was not in your cart")
    else:
        messages.info(request, "You don't have an active order")

    return redirect("cart_details")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)
    order_qs = ShoppingCart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                item.quantity += 1  # Increase available quantity when a single item is removed from cart
                item.save()
            else:
                order.items.remove(order_item)
                item.quantity += 1  # Increase available quantity when a single item is removed from cart
                item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart_details")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart_details")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart_details")


@login_required
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Products, slug=slug)

    if item.quantity <= 0:
        messages.error(request, "This item is out of stock.")
        return redirect("product_details", slug=slug)

    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = ShoppingCart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            item.quantity -= 1  # Reduce available quantity when a single item is added to cart
            item.save()
            messages.info(request, "This item quantity was updated")

        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            item.quantity -= 1  # Reduce available quantity when a single item is added to cart
            item.save()
    else:
        ordered_date = timezone.now()
        order = ShoppingCart.objects.create(
            user=request.user,
            ordered_date=ordered_date,
        )
        order.items.add(order_item)
        item.quantity -= 1  # Reduce available quantity when a single item is added to cart
        item.save()
        messages.info(request, "This item was added to your cart")

    return redirect("cart_details")


class ShoppingCartSummary(auth_mixins.LoginRequiredMixin, views.View):
    def get(self, *args, **kwargs):
        try:
            order = ShoppingCart.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order
            }
            return render(self.request, "cart/cart_details.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You dont have an active order")
            return render(self.request, "cart/cart_details.html")


class StaffOrdersListView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.ListView):
    model = ShoppingCart
    template_name = 'cart/staff_orders_list.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = ShoppingCart.objects.filter(ordered=True)
        order_by = self.request.GET.get('order_by', '-ordered_date')

        search_query = self.request.GET.get('Search')
        if search_query:
            initial_queryset = queryset.filter(
                Q(title__icontains=search_query)
            )
        else:
            initial_queryset = queryset

        if order_by == 'status':
            queryset = initial_queryset.order_by('status')
        elif order_by == 'ordered_date':
            queryset = initial_queryset.order_by('-ordered_date')

        # elif order_by == 'pending':
        #     queryset = initial_queryset.filter(status='pending')
        # elif order_by == 'sent':
        #     queryset = initial_queryset.filter(status='sent')
        # elif order_by == 'completed':
        #     queryset = initial_queryset.filter(status='completed')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order_by'] = self.request.GET.get('order_by', '-ordered_date')
        context['search_query'] = self.request.GET.get('Search', '')

        return context


class StaffOrderEditView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.UpdateView):
    queryset = ShoppingCart.objects.filter(ordered=True)
    template_name = "cart/staff_edit_order.html"
    fields = ('status',)

    def get_success_url(self):
        return reverse('staff_orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['order'] = self.object
        shipping_address = ShippingAddress.objects.filter(user=self.request.user).first()

        context['shipping_address'] = shipping_address

        return context
