from django.contrib.auth import views as auth_views, get_user_model, logout, login
from django.contrib.auth import forms as auth_forms
from django.forms import DateInput
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.shortcuts import redirect, render
from django.contrib.auth import mixins as auth_mixins

from alfa_romeo_web.accounts.forms import AlfaRomeoUserCreationForm, CustomAuthenticationForm
from alfa_romeo_web.accounts.mixin import OwnerRequiredMixin, CheckAdminOrStaffAccess
from alfa_romeo_web.accounts.models import Profile
from alfa_romeo_web.cart.models import ShoppingCart
from alfa_romeo_web.checkout.models import ShippingAddress

UserModel = get_user_model()


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/sign_in_user.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm


class RegisterUserView(views.CreateView):
    form_class = AlfaRomeoUserCreationForm
    template_name = 'accounts/register_user.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        # `form_valid` will call `save`
        result = super().form_valid(form)

        login(self.request, form.instance)

        return result


def logout_view(request):
    logout(request)
    return redirect('main_page')


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, views.DetailView):
    queryset = (Profile.objects.prefetch_related('user').all())
    template_name = "accounts/profile_details.html"
    fields = ("first_name", "last_name", "date_of_birth", 'phone_number', "profile_picture")


class ProfileEditView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, views.UpdateView):
    queryset = Profile.objects.all()
    template_name = "accounts/profile_edit.html"
    fields = ("first_name", "last_name", "date_of_birth", 'phone_number', "profile_picture")

    def get_success_url(self):
        return reverse('details-profile', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        form.fields["first_name"].label = "First Name"

        form.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        form.fields["last_name"].label = "Last Name"

        form.fields["date_of_birth"].widget.attrs["placeholder"] = "YYYY-MM-DD"
        form.fields["date_of_birth"].widget = DateInput(attrs={'type': 'date'})
        form.fields["date_of_birth"].label = "Birthday"

        form.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        form.fields["phone_number"].label = "Phone Number"

        form.fields["profile_picture"].widget.attrs["placeholder"] = "https://"
        form.fields["profile_picture"].label = "Profile Picture"

        return form


class ProfileChangePasswordView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, auth_views.PasswordChangeView):
    form_class = auth_forms.PasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy('main_page')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["old_password"].widget.attrs["placeholder"] = "Old Password"
        form.fields["old_password"].label = "Old Password"
        form.fields["old_password"].required = True

        form.fields["new_password1"].widget.attrs["placeholder"] = "New Password"
        form.fields["new_password1"].label = "New Password"
        form.fields["new_password1"].required = True

        form.fields["new_password2"].widget.attrs["placeholder"] = "Confirm New Password"
        form.fields["new_password2"].label = "Confirm New Password"
        form.fields["new_password2"].required = True

        return form


class ProfileDeleteView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, views.DeleteView):
    model = UserModel
    queryset = Profile.objects.all()
    template_name = "accounts/profile_delete.html"
    success_url = reverse_lazy('main_page')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return redirect(self.get_success_url())


class ProfileOrdersView(auth_mixins.LoginRequiredMixin, OwnerRequiredMixin, views.ListView):
    model = ShoppingCart
    template_name = "accounts/profile_orders.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = ShoppingCart.objects.filter(user=self.request.user, ordered=True).order_by('-ordered_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shipping = ShippingAddress.objects.filter(user=self.request.user)
        context['shipping'] = shipping
        return context


class StaffPanelView(auth_mixins.LoginRequiredMixin, CheckAdminOrStaffAccess, views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/staff_panel.html')
