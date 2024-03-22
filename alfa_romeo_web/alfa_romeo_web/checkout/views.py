from django.urls import reverse
from django.views import generic as views

from alfa_romeo_web.accounts.mixin import OwnerRequiredMixin
from alfa_romeo_web.accounts.models import Profile


class ProfileEditView(OwnerRequiredMixin, views.UpdateView):
    queryset = Profile.objects.all()
    template_name = "checkout/checkout_user.html"
    fields = ("first_name", "last_name", 'phone_number')

    def get_success_url(self):
        return reverse('details-profile', kwargs={'pk': self.object.pk})
        # return reverse('details-profile', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        form.fields["first_name"].label = "First Name"

        form.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        form.fields["last_name"].label = "Last Name"

        form.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        form.fields["phone_number"].label = "Phone Number"

        return form
