from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import redirect
from utils.Select import Selects


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is superuser or coordinator."""
    login_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.role != 'is_coordinator':
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class UserUrlCorrectMixin(AccessMixin):
    """Verify that the user is in correct application"""

    def dispatch(self, request, *args, **kwargs):
        url = f'/{request.META.get("PATH_INFO").split("/")[1].lower()}/'
        url_user = Selects().level_user_url()
        if url_user.get(request.user.level) != url:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
