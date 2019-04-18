from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from utils.Select import Selects

class VerifyChagePassword(MiddlewareMixin):
    """
    This middleware cheka si el usuario si cambio su contraseña
    """

    def process_view(self, request, view, *args, **kwargs):
        route_password = reverse("authentication:change_password")
        logout = request.META.get('PATH_INFO').split("/")[1].lower()
        if request.user.is_authenticated:
            if (not request.user.change_pass and
                    request.META.get('PATH_INFO') != route_password and
                    logout != 'logout'):
                return HttpResponseRedirect(route_password)


class VerifyQuestion(MiddlewareMixin):
    """
    This middleware cheka si el usuario tiene pregunta de seguridad 
    """

    def process_view(self, request, view, *args, **kwargs):
        route_question = reverse(
            "authentication:security_question", args=[request.user.pk])
        logout = request.META.get('PATH_INFO').split("/")[1].lower()
        if request.user.is_authenticated:
            if (request.user.change_pass and not request.user.question and
                request.META.get('PATH_INFO') != route_question and
                    logout != 'logout'):
                return HttpResponseRedirect(route_question)


class VerifyRoleUser(MiddlewareMixin):
    pass
#     def process_request(self, request, *args, **kwargs):
#         url = f'/{request.META.get("PATH_INFO").split("/")[1].lower()}/'
#         user = request.user
#         url_user = Selects().level_user_url()
#         if (user.is_superuser or user.role == "is_coordinator"):
#             k_url = 'is_admin_or_coordinator'

#         print(role_user.role,
#               role_user.level)
#         pass
