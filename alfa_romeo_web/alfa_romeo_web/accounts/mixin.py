from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import redirect


class OwnerRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if obj and obj.pk != request.user.pk:
                return self.handle_no_permission()
        else:
            try:
                pk = self.kwargs['pk']
                if request.user.pk != pk:
                    return self.handle_no_permission()
            except KeyError:
                raise Http404("No pk found in URL.")

        return super().dispatch(request, *args, **kwargs)


class CheckAdminOrStaffAccess:

    def dispatch(self, request, *args, **kwargs):
        data = super().dispatch(request, *args, **kwargs)
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect('main_page')

        return data
