from django.core import serializers
from sanidad.models import TypeCompany, Company
import json

def get_type_company_report(type_company, date, week1, week2):
    data = []
    inspection_total = 0
    type_companys = TypeCompany.objects.all()
    if type_company != "all":
        type_companys = type_companys.filter(pk=type_company)
    for key, tp_company in enumerate(type_companys):
        data.append(dict(
            type_company=tp_company.name,
            companys=list(),
            inspection_total=inspection_total
        )),
        companys = Company.objects.filter(type_company=tp_company)
        for company in companys:
            inspections = company.get_inspections()
            if date:
                inspections = company.get_inspections(week1, week2)
            inspection_total += len(inspections)
            inspections = serializers.serialize(
                'json', inspections,
                fields=('date', 'result',
                        'next_date', 'notes',))
            data[key]['companys'].append(dict(
                name=company.get_full_name(),
                inspections=json.loads(inspections)
            ))
        data[key]['inspection_total'] = inspection_total
        inspection_total = 0
    return data


def get_company_report(company, date, week1, week2):
    data = []
    inspection_total = 0
    companys = Company.objects.all()
    if company != 'all':
        companys = companys.filter(pk=company)
    for key, compan in enumerate(companys):
        data.append(dict(
            type_company=compan.type_company.name,
            companys=list(),
            inspection_total=inspection_total
        ))
        inspections = compan.get_inspections()
        if date:
            inspections = compan.get_inspections(week1, week2)
        inspection_total = len(inspections)
        inspections = serializers.serialize(
            'json', inspections,
            fields=('date', 'result',
                    'next_date', 'notes',))
        data[key]['companys'].append(dict(
            name=compan.get_full_name(),
            inspections=json.loads(inspections)
        ))
        data[key]['inspection_total'] = inspection_total
    return data