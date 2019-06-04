from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from core.models import Municipality, Parish
from django.views.generic import View, TemplateView
from authentication.models import User
from acuicultura.models import ProductionUnit
from sanidad import models
from datetime import timedelta, datetime, date
from utils.get_data_report import get_company_report, get_type_company_report, \
    get_driver_report, get_inspections_expired
# Create your views here.


class ApiMunicipalityView(View):
    model = Municipality

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = self.model.objects.filter(state__pk=pk)
        data = serializers.serialize(
            "json", data)
        return JsonResponse(data, safe=False)


class ApiParishView(View):
    model = Parish

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        data = self.model.objects.filter(municipality__pk=pk)
        data = serializers.serialize(
            "json", data)
        return JsonResponse(data, safe=False)


class HomeTemplateView(TemplateView):
    template_name = "home_template_view.html"

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        # user
        context['user'] = User.objects.filter(
            is_delete=False, is_superuser=False).exclude(email=self.request.user.email)
        
        # acuicultuta
        context['acuicultura'] = ProductionUnit.objects.all()[:5]
        
        # sanidad
        today = datetime.now()
        start = today - timedelta(days=10)
        end = today + timedelta(days=10)
        context['company'] = models.Company.objects.filter(is_inspection=True)
        context['driver'] = models.Driver.objects.filter(is_inspection=True)
        inspection = models.Inspection.objects.filter(
            next_date__range=(start, end), pass_inspection=False)
        inspection_list = []
        for i in inspection:
            if i.company_account.is_inspection:
                inspection_list.append(i)
        context['inspection'] = inspection_list
        context['inspection_expired'] = len(get_inspections_expired())
        years = datetime.now().year
        context['year_list'] = [i for i in range(years - 5, years+1)][::-1]
        return context
    

class HelpView(TemplateView):
    template_name = "help.html"
