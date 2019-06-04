from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from utils.Select import Selects
from django.urls import reverse


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is superuser or coordinator."""
    login_url = '/'

    def dispatch(self, request, *args, **kwargs):
        path = request.META.get('PATH_INFO')
        detail = reverse('authentication:detail_profile')
        update = reverse('authentication:update_profile')

        if (path == detail or path == update):
            pass
        elif not request.user.is_superuser and request.user.role != 'is_coordinator':
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class UserUrlCorrectMixin(AccessMixin):
    """Verify that the user is in correct application"""

    def dispatch(self, request, *args, **kwargs):
        url = f'/{request.META.get("PATH_INFO").split("/")[1].lower()}/'
        url_user = Selects().level_user_url()
        # if (url_user.get(request.user.level) != url and not request.user.is_superuser and not request.user.role == 'is_coordinator'):
        #     return redirect('/')
        return super().dispatch(request, *args, **kwargs)
