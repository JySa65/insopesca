from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.sites.shortcuts import get_current_site


def checkUserLogin(sender, user, request, **kwargs):
    current_site = get_current_site(request)
    user.ip = current_site.domain
    user.is_login = True
    user.save()


user_logged_in.connect(checkUserLogin)


def checkUserLogout(sender, user, request, **kwargs):
    user.is_login = False
    user.save()
    print("se ejecuta")


user_logged_out.connect(checkUserLogout)
