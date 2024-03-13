from django.contrib.auth.mixins import AccessMixin


class OwnerRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs.get('pk', None):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)