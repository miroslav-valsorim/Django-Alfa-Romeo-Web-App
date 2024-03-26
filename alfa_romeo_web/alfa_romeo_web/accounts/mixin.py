from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OwnerRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        data = super().dispatch(request, *args, **kwargs)

        if request.user.pk != kwargs.get('pk', None):
            return self.handle_no_permission()
        return data


class CheckAdminOrStaffAccess:

    def dispatch(self, request, *args, **kwargs):
        data = super().dispatch(request, *args, **kwargs)
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect('main_page')

        return data
