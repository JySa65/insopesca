from django.core import serializers
from sanidad.models import TypeCompany, Company, Driver
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
                fields=('date', 'result', 'account_register',
                        'next_date', 'notes',),  use_natural_foreign_keys=True, use_natural_primary_keys=True)
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
            fields=('date', 'result', 'account_register',
                    'next_date', 'notes',),  use_natural_foreign_keys=True, use_natural_primary_keys=True)
        data[key]['companys'].append(dict(
            name=compan.get_full_name(),
            inspections=json.loads(inspections)
        ))
        data[key]['inspection_total'] = inspection_total
    return data


def get_driver_report(driver, date, week1, week2):
    data = []
    inspection_total = 0
    drivers = Driver.objects.all()
    if driver != 'all':
        drivers = drivers.filter(pk=driver)
    for key, compan in enumerate(drivers):
        data.append(dict(
            type_company="Conductor",
            companys=list(),
            inspection_total=inspection_total
        ))
        inspections = compan.get_inspections()
        if date:
            inspections = compan.get_inspections(week1, week2)
        inspection_total = len(inspections)
        inspections = serializers.serialize(
            'json', inspections,
            fields=('date', 'result', 'account_register',
                    'next_date', 'notes',), use_natural_foreign_keys=True, use_natural_primary_keys=True)
        data[key]['companys'].append(dict(
            name=compan.get_full_name(),
            inspections=json.loads(inspections)
        ))
        data[key]['inspection_total'] = inspection_total
    return data


def get_inspections_expired():
    data = []
    companys = Company.objects.filter(is_inspection=False)
    drivers = Driver.objects.filter(is_inspection=False)
    for company in companys:
        inspection = company.get_inspections().first()
        data.append(dict(
            type_company=company.type_company.name,
            name=company.get_full_name(),
            document=company.get_document(),
            tlf=company.tlf,
            is_active=company.is_active,
            inspection=dict(
                date=inspection.date,
                pass_date=inspection.next_date,
                user=inspection.account_register.email,
                result=inspection.result,
                notes=inspection.notes
            ) if inspection else []
        ))
    for driver in drivers:
        inspection = driver.get_inspections().first()
        data.append(dict(
            type_company='Conductor',
            name=driver.get_full_name(),
            document=driver.get_document(),
            tlf=driver.tlf,
            is_active=driver.is_active,
            inspection=dict(
                date=inspection.date,
                pass_date=inspection.next_date,
                user=inspection.account_register.email,
                result=inspection.result,
                notes=inspection.notes
            ) if inspection else []
        ))
    return data
