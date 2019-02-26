from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from core.models import Municipality, Parish
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
# Create your views here.


class ApiMunicipalityView(LoginRequiredMixin, View):
    model = Municipality

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = self.model.objects.filter(state__pk=pk)
        data = serializers.serialize(
            "json", data)
        return JsonResponse(data, safe=False)


class ApiParishView(LoginRequiredMixin, View):
    model = Parish

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = self.model.objects.filter(municipality__pk=pk)
        data = serializers.serialize(
            "json", data)
        return JsonResponse(data, safe=False)
