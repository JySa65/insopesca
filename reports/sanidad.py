from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from reports.base import PDF, FILENAME
from utils.alert import alert
from sanidad import models


class ReportSanidadListInpections(View):

    def valid_type(self, typei):
        if typei not in ['driver', 'company']:
            return False
        return True

    def valid_date(self, date1, date2):
        if date1 > date2:
            return False, None, None
        return True, date1, date2

    def set_data(self):
        typei = self.request.GET.get('type', '')
        if not self.valid_type(typei):
            return False, None
        status, date1, date2 = self.valid_date(
            self.request.GET.get('date1', ''),
            self.request.GET.get('date2', ''))
        if status == False:
            return False, None
        model = models.Company if typei == "company" else models.Driver
        data_list = []
        datas = model.objects.filter(is_inspection=True)
        for data in datas:
            if date1 != "" and date2 != "":
                inspection = models.Inspection.objects.filter(
                    company_account_id=data.pk,
                    date__range=(date1, date2)).first()
            else:
                inspection = models.Inspection.objects.filter(
                    company_account_id=data.pk).first()
            if inspection:
                data_list.append(dict(
                    data=data,
                    inspection=inspection
                ))
        return True, data_list

    def get(self, *args, **kwargs):
        status, data = self.set_data()
        if not status:
            return alert("Algo Esta Haciendo Mal Que No Se Pudo Generar El PDF")
        if len(data) == 0:
            return alert("No Hay Nada Que Mostrar")
        cont = 1
        pdf = PDF('L', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        name_title = "Empresas" if self.request.GET.get('type', '') == 'company' else 'Conductores'
        pdf.cell(0, 0, f'Lista de {name_title} Inspeccionados', 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(7.9, 8, '#', 1, 0, 'C')
        pdf.cell(40, 8, 'Documento', 1, 0, 'C')
        pdf.cell(80, 8, 'Nombre', 1, 0, 'C')
        pdf.cell(50, 8, 'Fecha De Inspección', 1, 0, 'C')
        pdf.cell(50, 8, 'Proxima Inspección', 1, 0, 'C')
        pdf.cell(45, 8, 'Resultado', 1, 1, 'C')
        for i in data:
            document = i.get('data').get_document()
            name = i.get('data').get_full_name()
            date = str(i.get('inspection').date)
            next_date = str(i.get('inspection').next_date)
            status_result = i.get('inspection').result
            result = 'Muy Bueno' if status_result == "is_verygood" else 'Bueno' if status_result == "is_good" else 'Malo'
            pdf.cell(7.9, 8, str(cont), 1, 0, 'C')
            pdf.cell(40, 8, document, 1, 0, 'C')
            pdf.cell(80, 8, name, 1, 0, 'C')
            pdf.cell(50, 8, date, 1, 0, 'C')
            pdf.cell(50, 8, next_date, 1, 0, 'C')
            pdf.cell(45, 8, result, 1, 1, 'C')
            cont += 1
        pdf.set_font('Arial', '', 12)
        pdf.cell(265, 8, f'Total De Inspecciones: {len(data)}', 0, 1, 'R')
        pdf.output(FILENAME, 'F')
        fs = FileSystemStorage()
        with fs.open(FILENAME) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response


# class 


class ReportCompanyAll(View):

    def get(self, *args, **kwargs):
        typei = self.request.GET.get('typei', '')
        companys = models.Company.objects.all()
        cont = 1
        pdf = PDF('L', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(7.9, 8, '#', 1, 0, 'C')
        pdf.cell(40, 8, 'Nombre', 1, 0, 'C')
        pdf.cell(40, 8, 'Telefono', 1, 1, 'C')

        pdf.output(FILENAME, 'F')
        fs = FileSystemStorage()
        with fs.open(FILENAME) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response



