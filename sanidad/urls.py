from django.urls import path
from sanidad.views import sview
app_name = 'sanidad'
urlpatterns = [
    path('', sview, name="list")
]
