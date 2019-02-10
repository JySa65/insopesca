"""insopesca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication.views import LoginFormView, ForgotPassword
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('authentication/', include(
        'authentication.urls', namespace="authentication")),
    path('forgot-password/', ForgotPassword.as_view(), name="forgot_password"),
    path("acuicultura/", include(
        'acuicultura.urls', namespace="acuicultura"))

]
