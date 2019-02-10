from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.


def sview(request):
    return render(request, 'hola.html')
