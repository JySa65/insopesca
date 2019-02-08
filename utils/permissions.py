from django.contrib.auth.mixins import AccessMixin


class AdminRequiredMixin(AccessMixin):
    # permission_denied_message = 'Se ha autenticado como joselacruz, pero no está autorizado a acceder a esta página. ¿Desea autenticarse con una cuenta diferente?'

    """Verify that the current user is superuser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
