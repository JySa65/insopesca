from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse


class VerifyQuestionAndChagePassword(MiddlewareMixin):
    """
    This middleware cheka si el usuario tiene pregunta de seguridad 
    y si cambio su contraseña
    """

    def process_view(self, request, view, *args, **kwargs):
        # route_password = reverse("authentication:change_password")
        # route_question = reverse()
        # if request.user.is_authenticated:
        #     if (not request.user.change_pass and
        #             request.META.get('PATH_INFO') != route_password):
        #         return HttpResponseRedirect(route_password)
        #     if not request.user.question:
        #         print("No a registrado pregunta de seguridad")
        return None
        # print(request.META.get('PATH_INFO').split("/")[1].lower())
        # raise Http404


class RequestUserValidUrl(MiddlewareMixin):
    """
    This middleware expire token pass the 5 hours
    """

    def process_view(self, request, view, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return None
        return None
        # print(request.META.get('PATH_INFO').split("/")[1].lower())
        # raise Http404
