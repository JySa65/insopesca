import time
import calendar
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, colors, Alignment, Border, Side
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from isoweek import Week
from sanidad.models import TypeCompany, Company
from utils.date_insopesca import DateInsopesca
from utils.get_data_report import get_type_company_report
FILENAME = f'{settings.MEDIA_ROOT}/reports_excel.xlsx'


class InpectionsCompany(View):
    def get(self, request, *args, **kwargs):
        companys, type_companys = self.get_data()
        return self.form(companys, type_companys)
        # fs = FileSystemStorage()
        # with fs.open(FILENAME) as xlsx:
        #     response = HttpResponse(xlsx)
        #     response['Content-type'] = 'application/ms-excel'
        #     response['Content-Disposition'] = 'inline; filename="reporte_excel.xlsx"'
        # return response

    def form(self, companys, type_companys):
        wb = Workbook()
        ws = wb.active

        # title
        thin = Side(border_style="thin", color="010204")

        ws.row_dimensions[1].height = 40
        ws.merge_cells('A1:M1')
        ws.cell(row=1, column=1).value = "Inspecciones Sanitarias Insopesca"
        ws.cell(row=1, column=1).border = Border(bottom=thin)
        ws.cell(row=1, column=13).border = Border(right=thin)
        ws.cell(row=1, column=1).font = Font(
            size=30, name='Arial', color='5969ff', bold=True)
        ws.cell(row=1, column=1).alignment = Alignment(
            horizontal="center", vertical="center")

        #  week
        ws.row_dimensions[3].height = 20
        ws.column_dimensions['A'].width = 28
        ws.merge_cells('A3:A4')
        ws.cell(row=3, column=1).value = "Semana"
        ws.cell(row=3, column=1).border = Border(top=thin, left=thin, right=thin)
        ws.cell(row=4, column=1).border = Border(bottom=thin)
        ws.cell(row=3, column=1).font = Font(
            size=14, name='Arial', bold=True)
        ws.cell(row=3, column=1).alignment = Alignment(
            horizontal="center", vertical="center")
        
        ws.merge_cells('B3:M3')
        ws.cell(row=3, column=2).value = "Tipo De Compañia"
        ws.cell(row=3, column=2).border = Border(bottom=thin, top=thin, left=thin)
        ws.cell(row=3, column=13).border = Border(right=thin)
        ws.cell(row=3, column=2).font = Font(
            size=14, name='Arial', bold=True)
        ws.cell(row=3, column=2).alignment = Alignment(
            horizontal="center", vertical="center")

        for key, type_company in enumerate(type_companys):
            col = key + 2
            row = 4
            value = type_company['name'].title()
            ws.column_dimensions[get_column_letter(col)].width = len(value) * 2
            ws.cell(row=row, column=col).value = value
            ws.cell(row=row, column=col).border = Border(
                bottom=thin, top=thin, left=thin, right=thin)
            ws.cell(row=row, column=col).font = Font(
                size=14, name='Arial', bold=True)
            ws.cell(row=row, column=col).alignment = Alignment(
                horizontal="center", vertical="center")
        
        print(companys)
        for k, company in enumerate(companys):
            value = company['range_week']
            row = k + 5
            ws.cell(row=row, column=1).value = value
            ws.cell(row=row, column=1).border = Border(
                bottom=thin, top=thin, left=thin, right=thin)
            ws.cell(row=row, column=1).font = Font(
                size=11, name='Arial')
            ws.cell(row=row, column=1).alignment = Alignment(
                horizontal="center", vertical="center")
            
            for key, total in enumerate(company['inspections_total']):
                col = (key) + 2
                value = total
                ro = key + row
                ws.cell(row=ro, column=col).value = value
                ws.cell(row=ro, column=col).border = Border(
                    bottom=thin, top=thin, left=thin, right=thin)
                ws.cell(row=ro, column=col).font = Font(
                    size=11, name='Arial', bold=True)
                ws.cell(row=ro, column=col).alignment = Alignment(
                    horizontal="center", vertical="center")
        wb.save(FILENAME)
        return HttpResponse("si")

    def get_data(self):
        type_comanys = [dict(pk=i.pk, name=i.name)
                        for i in TypeCompany.objects.all()]
        data = []
        _range = Week.last_week_of_year(2019)[1]
        for i in range(_range):
            first, last = DateInsopesca('2019', i+1).get_date_range_from_week()
            data.append(dict(
                range_week=f'{first} a {last}',
                inspections_total=[]))
            for type_comany in type_comanys:
                inspection_total = 0
                companys = Company.objects.filter(type_company=type_comany['pk'])
                for company in companys:
                    inspections = company.get_inspections('2019-20', '2019-20')
                    inspection_total += len(inspections)
                data[0]['inspections_total'].append(inspection_total)
        return data, type_comanys
