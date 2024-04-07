import uuid

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required

from paypal.standard.forms import PayPalPaymentsForm

from alfa_romeo_web.accounts.mixin import OwnerRequiredMixin
from alfa_romeo_web.accounts.models import Profile
from alfa_romeo_web.cart.models import ShoppingCart
from alfa_romeo_web.checkout.forms import CheckoutForm
from alfa_romeo_web.checkout.models import ShippingAddress


class ProfileEditView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, views.UpdateView):
    queryset = Profile.objects.all()
    template_name = "checkout/checkout_user.html"
    fields = ("first_name", "last_name", 'phone_number')

    def get_success_url(self):
        return reverse('second_step', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        form.fields["first_name"].label = "First Name"

        form.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        form.fields["last_name"].label = "Last Name"

        form.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        form.fields["phone_number"].label = "Phone Number"

        return form


class CheckoutView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, views.View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout/checkout_user_two.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = ShoppingCart.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                shipping_address = form.cleaned_data['shipping_address']
                shipping_address_two = form.cleaned_data['shipping_address_two']
                country = form.cleaned_data['country']
                town = form.cleaned_data['town']
                zip_code = form.cleaned_data['zip']

                shipping_address = ShippingAddress(
                    user=self.request.user,
                    shipping_address=shipping_address,
                    shipping_address_two=shipping_address_two,
                    country=country,
                    town=town,
                    zip=zip_code,
                )
                shipping_address.save()
                order.shipping_address = shipping_address
                order.save()

                return redirect('payment')

            messages.warning(self.request, 'Failed Checkout, some of the fields are improperly formatted')

            # TODO handle form validation messages, (doesn't appear for some reason?)

            return redirect(reverse('second_step', kwargs={'pk': self.request.user.pk}))

        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have active order")
            return redirect("cart_details")


class PaymentView(auth_mixins.LoginRequiredMixin, views.TemplateView):
    template_name = 'checkout/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(ShoppingCart, user=self.request.user, ordered=False)
        host = self.request.get_host()

        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': order.get_total(),
            'item_name': order.id,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('paypal_payment_successful', kwargs={'shopping_cart_id': order.id})}",
            'cancel_url': f"http://{host}{reverse('paypal_payment_failed', kwargs={'shopping_cart_id': order.id})}",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context['order'] = order
        context['paypal'] = paypal_payment
        return context


@login_required
def paypal_payment_successful(request, shopping_cart_id):
    # in case the success payment work properly there is more things to be set
    # info here https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
    # signals should be made + installing  https://ngrok.com/
    # more info here https://www.youtube.com/watch?v=Ftz3DG9Sq50&ab_channel=ZackPlauch%C3%A9
    # if request.method == "POST":
    #     # Handle PayPal IPN notification
    #     # Verify the IPN data and update your database accordingly
    #     # Sample code to handle IPN data
    #     ipn_data = request.POST
    #     status = ipn_data['payment_status']
    #     if status == 'Completed':
    #         # Update your database to mark the order as paid
    cart_id = ShoppingCart.objects.get(id=shopping_cart_id)
    order = ShoppingCart.objects.get(user=request.user, ordered=False)
    order.ordered = True
    order.save()

    order_items = order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()

    context = {
        'cart_id': cart_id.id,
    }

    return render(request, 'checkout/payment-success.html', context)


@login_required
def paypal_payment_failed(request, shopping_cart_id):
    cart_id = ShoppingCart.objects.get(id=shopping_cart_id)

    context = {
        'cart_id': cart_id.id,
    }

    return render(request, 'checkout/payment-failed.html', context)
