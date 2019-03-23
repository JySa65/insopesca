from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse


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
