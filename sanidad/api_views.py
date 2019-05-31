from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from sanidad import models
from datetime import datetime


class ChartMonthReportAPIView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        data = [
            dict(name="Muy Bueno", bg="#28a745",
                 bd="#01751b", data=[]),
            dict(name="Bueno", bg="#007bff",
                 bd="#3b98da", data=[]),
            dict(name="Malo", bg="#dc3545",
                 bd="#73000b", data=[]),
        ]
        very_good = 0
        good = 0
        bad = 0
        year = self.request.GET.get('year')
        if year == "":
            year = datetime.now().year
        for month in range(12):
            inspections = models.Inspection.objects.filter(
                date__year=year, date__month=month+1)
            for inspection in inspections:
                if inspection.result == "is_verygood":
                    very_good += 1
                elif inspection.result == "is_good":
                    good += 1
                else:
                    bad += 1
            data[0]['data'].append(very_good)
            data[1]['data'].append(good)
            data[2]['data'].append(bad)
            very_good = 0
            good = 0
            bad = 0
        return JsonResponse(data, safe=False)


class ChartInspectionsDriverAndCompany(View):

    def get(self, *args, **kwargs):
        year = self.request.GET.get('year', '')
        if year == "":
            year = datetime.now().year
        companys = models.Company.objects.all()
        drivers = models.Driver.objects.all()
        data = [
            dict(name="Empresas", data=0),
            dict(name="Conductores", data=0)
        ]
        for company in companys:
            inspection = models.Inspection.objects.filter(
                date__year=year, company_account_id=company.pk)
            data[0]['data'] += inspection.count()

        for driver in drivers:
            inspection = models.Inspection.objects.filter(
                date__year=year, company_account_id=driver.pk)
            data[1]['data'] += inspection.count()

        return JsonResponse(data, safe=False)


class ChartInspectionsType(View):
    def get(self, *args, **kwargs):
        data = dict(
            name=[],
            data=[]
        )
        year = self.request.GET.get('year', '')

        if year == "":
            year = datetime.now().year

        type_companys = models.TypeCompany.objects.all()
        drivers = models.Driver.objects.all()

        for type_company in type_companys:
            acum = 0
            companys = type_company.company_set.all()
            for company in companys:
                inspection = models.Inspection.objects.filter(
                    date__year=year, company_account_id=company.pk)
                acum += inspection.count()
            data['name'].append(type_company.name)
            data['data'].append(acum)
        
        acum = 0        
        for driver in drivers:
            inspection = models.Inspection.objects.filter(
                date__year=year, company_account_id=driver.pk)
            acum += inspection.count()
        data['name'].append('conductor')
        data['data'].append(acum)

        return JsonResponse(data, safe=False)
