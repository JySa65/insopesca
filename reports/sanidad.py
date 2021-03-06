from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date
from reports.base import PDF, FILENAME, PDFL
from utils.alert import alert
from sanidad import models
from utils.get_data_report import get_company_report, get_type_company_report, \
    get_driver_report, get_inspections_expired
from utils.validate_uuid import validate_uuid4

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
        pdf = PDFL('L', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        name_title = "Empresas" if self.request.GET.get(
            'type', '') == 'company' else 'Conductores'
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


class ReportListCompanyOrDriver(View):
    def valid_type(self, typei):
        if typei not in ['all_company', 'all_driver']:
            return False
        return True


    def set_data(self):
        report_select = self.request.GET.get('typei', '')
        date_1 = self.request.GET.get('date1', '')
        date_2 = self.request.GET.get('date2', '')
        status = self.valid_type(report_select)
        valid = self.request.GET.get('valid', '0')
        values = None
        dates = None

        model = models.Company if report_select == "all_company" else models.Driver
        if valid == "1":
            if date_1 != '':
                start = datetime.strptime((date_1), "%d/%m/%Y").strftime("%Y-%m-%d %H:%M")
                end = datetime.today()
            if date_2 != "":
                end = datetime.strptime((date_2+" 23:59"), 
                                            "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
            if date_1 !="":
                if str(end) <= str(start):
                    values = False

            else:
                dates = False
                
        if (date_1) == '':
            datas = model.objects.all()
        else:
            datas = model.objects.filter(created_at__range=(start, end))
        return status, datas, model,values,dates

    def get(self, *args, **kwargs):
        status, data, _type,val,dates_value = self.set_data()

        if status == False:
            return alert("Algo Esta Haciendo Mal Que No Se Pudo Generar El PDF")
        if dates_value == False:
            return alert("Por Favor declare Las Fechas,.")
        if val == False:
            return alert("Rango de Fechas Incoherente.")

        if len(data) == 0:
            alert("No hay nada que mostrar")

        cont = 1
        pdf = PDFL('L', 'mm', 'A4')
        if _type != models.Company: pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        name_title = "Empresas" if _type == models.Company else 'Conductores'
        pdf.cell(0, 0, f'Lista de {name_title}', 0, 1, 'C')
        pdf.ln(10)
        pdf.cell(7.9, 8, '#', 1, 0, 'C')
        pdf.cell(40, 8, 'Documento', 1, 0, 'C')
        (pdf.cell(120, 8, 'Nombre', 1, 0, 'C') if _type == models.Company else
         pdf.cell(90, 8, 'Nombres y Apellidos', 1, 0, 'C'))
        pdf.cell(35, 8, 'Telefono Movil', 1, 0, 'C')

        if _type == models.Company:
            pdf.cell(35, 8, 'SPES', 1, 0, 'C')
            pdf.cell(40, 8, 'Activo', 1, 1, 'C')
            pdf.set_font('Arial', '', 11)
            for i in data:
                document = i.get_document()
                name = i.get_full_name()
                tlf = i.tlf
                spes = i.speg
                status = i.is_active
                result = 'Si' if status == True else 'No'

                pdf.cell(7.9, 8, str(cont), 1, 0, 'C')
                pdf.cell(40, 8, document, 1, 0, 'C')
                pdf.cell(120, 8, name, 1, 0, 'C')
                pdf.cell(35, 8, tlf, 1, 0, 'C')
                pdf.cell(35, 8, spes, 1, 0, 'C')
                pdf.cell(40, 8, result, 1, 1, 'C')

                cont += 1
        else:
            pdf.cell(20, 8, 'Activo', 1, 1, 'C')
            pdf.set_font('Arial', '', 11)
            for i in data:
                document = i.get_document()
                name = i.get_full_name()
                tlf = i.tlf
                status = i.is_active
                result = 'Si' if status == True else 'No'

                pdf.cell(7.9, 8, str(cont), 1, 0, 'C')
                pdf.cell(40, 8, document, 1, 0, 'C')
                pdf.cell(90, 8, name, 1, 0, 'C')
                pdf.cell(35, 8, tlf, 1, 0, 'C')
                pdf.cell(20, 8, result, 1, 1, 'C')

                cont += 1
        
        position = 190 if _type != models.Company else 275
        pdf.cell(position, 8, f'Total De {name_title}: {len(data)}', 0, 1, 'R')
        pdf.output(FILENAME, 'F')
        fs = FileSystemStorage()
        with fs.open(FILENAME) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response


class ReportIndividualCompanyOrDriver(View):
    def valid_type(self, typei):
        if typei not in ['individual_company', 'individual_driver']:
            return False
        return True

    def set_data(self):
        report_select = self.request.GET.get('typei', '')
        ppk = self.request.GET.get('pk','')
        status = self.valid_type(report_select)
        valid_uui = validate_uuid4(ppk)

        model = models.Company if report_select == "individual_company" else models.Driver
        if valid_uui == True:
            company = model.objects.filter(pk=ppk)
        else:
            company = False

        return status, company, report_select,model,valid_uui

    def get(self, *args, **kwargs):
        status, data, _type,_mode,uui = self.set_data()
        if status == False:
            return alert("Algo Esta Haciendo Mal Que No Se Pudo Generar El PDF")
        if (data) == None:
            return alert("No Hay Nada Que Mostrar")
        if (uui) == False:
            return alert("Esta Haciendo Algo Raro :'c")

        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()

        pdf.set_font('Arial', 'B', 14)
        name_title = "DE LA EMPRESA " if _mode == models.Company else 'DEL CONDUCTOR'
        pdf.cell(0, 0, f'INFORMACIÓN {name_title}', 0, 1, 'C')
        pdf.set_font('Arial', 'B', 9)
        pdf.ln(10)
        cont = 1

        if _mode == models.Company:

            for i in data:

                pdf.cell(30, 10, 'DOCUMENTO', 1, 0, 'C')
                pdf.cell(155, 10, "TIPO DE COMAPAÑIA", 1, 1, "C")
                pdf.cell(30, 10, i.get_document(), 1, 0, "C")
                pdf.cell(155, 10, i.type_company.name.upper(), 1, 1, "C")
                pdf.cell(185, 10, "NOMBRE", 1, 1, "C") if _mode == models.Company else pdf.cell(
                    155, 10, "NOMBRE", 1, 1, "C")
                pdf.cell(185, 10, i.get_full_name(), 1, 1, "C")

                pdf.cell(92.5, 10, 'TELEFONO MOVIL', 1, 0, 'C')
                pdf.cell(92.5, 10, 'TELEFONO DE CASA', 1, 1, 'C')
                if i.tlf == None:
                    pdf.cell(92.5, 10, "NO POSEE", 1, 1, "C")
                else:
                    pdf.cell(92.5, 10, (i.tlf), 1, 0, "C")

                if i.tlf_house == None:
                    pdf.cell(92.5, 10, "NO POSEE", 1, 1, "C")
                else:
                    pdf.cell(92.5, 10, (i.tlf_house), 1, 1, "C")

                pdf.cell(61.6, 10, 'ESTADO', 1, 0, 'C')
                pdf.cell(61.6, 10, 'MUNICIPIO', 1, 0, 'C')
                pdf.cell(61.8, 10, 'PARROQUIA', 1, 1, 'C')

                pdf.cell(61.6, 10, (i.state.name.upper()), 1, 0, "C")
                pdf.cell(61.6, 10, (i.municipality.name.upper()), 1, 0, "C")
                pdf.cell(61.8, 10, (i.parish.name.upper()), 1, 1, "C")

                pdf.cell(185, 10, "DIRECCIÓN", 1, 1, "C")
                pdf.multi_cell(185, 5, i.address, 1, "J")

                pdf.ln(10)
                pdf.set_font('Arial', 'B', 14)

                name_second_title = "A LA EMPRESA " if _mode == models.Company else 'DEL CONDUCTOR'
                pdf.cell(
                    0, 0, f'INSPECCIONES REALIZADAS {name_second_title}', 0, 1, 'C')
                pdf.set_font('Arial', 'B', 9)

                pdf.ln(10)
                pdf.set_text_color(0, 0, 0)

                pdf.cell(10, 8, '#', 1, 0, 'C')
                pdf.cell(45, 8, 'FECHA DE INSPECCIÓN', 1, 0, 'C')
                pdf.cell(40, 8, 'RESULTADO', 1, 0, 'C')
                pdf.cell(90, 8, 'REALIZADO POR ', 1, 1, 'C')

                for x in i.get_inspections():

                    _date = x.date.strftime('%d/%m/%Y')
                    status_result = x.result
                    result = 'Muy Bueno' if status_result == "is_verygood" else 'Bueno' if status_result == "is_good" else 'Malo'

                    pdf.cell(10, 8, str(cont), 1, 0, 'C')
                    pdf.cell(45, 8, _date, 1, 0, 'C')
                    pdf.cell(40, 8, result, 1, 0, 'C')
                    pdf.cell(
                        90, 8, (x.account_register.get_full_name()), 1, 1, 'C')

                    cont += 1
        else:
            for i in data:
                pdf.cell(30, 10, 'DOCUMENTO', 1, 0, 'C')
                pdf.cell(155, 10, "NOMBRE", 1, 1, "C")
                pdf.cell(30, 10, i.get_document(), 1, 0, "C")
                pdf.cell(155, 10, i.get_full_name(), 1, 1, "C")

                pdf.cell(92.5, 10, 'TELEFONO MOVIL', 1, 0, 'C')
                pdf.cell(92.5, 10, 'TELEFONO DE CASA', 1, 1, 'C')
                if i.tlf == None:
                    pdf.cell(92.5, 10, "NO POSEE", 1, 1, "C")
                else:
                    pdf.cell(92.5, 10, (i.tlf), 1, 0, "C")

                if i.tlf_house == None:
                    pdf.cell(92.5, 10, "NO POSEE", 1, 1, "C")
                else:
                    pdf.cell(92.5, 10, (i.tlf_house), 1, 1, "C")

                pdf.cell(185, 10, "DIRECCIÓN", 1, 1, "C")
                pdf.multi_cell(185, 5, i.address, 1, "J")

                pdf.ln(10)
                pdf.set_font('Arial', 'B', 14)

                name_second_title = "A LA EMPRESA " if _mode == models.Company else 'DEL CONDUCTOR'
                pdf.cell(
                    0, 0, f'INSPECCIONES REALIZADAS {name_second_title}', 0, 1, 'C')
                pdf.set_font('Arial', 'B', 9)

                pdf.ln(10)
                pdf.set_text_color(0, 0, 0)

                pdf.cell(10, 8, '#', 1, 0, 'C')
                pdf.cell(45, 8, 'FECHA DE INSPECCIÓN', 1, 0, 'C')
                pdf.cell(40, 8, 'RESULTADO', 1, 0, 'C')
                pdf.cell(90, 8, 'REALIZADO POR ', 1, 1, 'C')

                for x in i.get_inspections():

                    _date = x.date.strftime('%d/%m/%Y')
                    status_result = x.result
                    result = 'Muy Bueno' if status_result == "is_verygood" else 'Bueno' if status_result == "is_good" else 'Malo'

                    pdf.cell(10, 8, str(cont), 1, 0, 'C')
                    pdf.cell(45, 8, _date, 1, 0, 'C')
                    pdf.cell(40, 8, result, 1, 0, 'C')
                    pdf.cell(
                        90, 8, (x.account_register.get_full_name()), 1, 1, 'C')

                    cont += 1

            pdf.ln()

        pdf.output(FILENAME, 'F')
        fs = FileSystemStorage()
        with fs.open(FILENAME) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response


class ReportInspectionGeneralView(View):

    def get(self, request, *args, **kwargs):
        type_company = request.GET.get('type_company', '')
        company = request.GET.get('company', '')
        driver = request.GET.get('driver', '')
        week1 = request.GET.get('week1', '')
        week2 = request.GET.get('week2', '')
        date = bool(int(request.GET.get('date')))

        if (type_company == "" and company == "" and driver == "" or
                type_company != "" and company != "" and driver != ""):
            return alert("Debes Escoger una compañia o un tipo de compañia o conductor")

        if date == 1:
            if week1 == "":
                return alert("Asignes Fecha Inicial Para La Consulta")
        
        if (type_company != 'all' and type_company != "" or
            company != "" and company != 'all' or 
            driver != "" and driver != 'all'):
            if (not validate_uuid4(type_company) and 
                not validate_uuid4(company) and not validate_uuid4(driver)):
                return alert("Esta Haciendo Algo Raro :'c")
        
        if type_company != '':
            data = get_type_company_report(type_company, date, week1, week2)

        if company != '':
            data = get_company_report(company, date, week1, week2)

        if driver != '':
            data = get_driver_report(driver, date, week1, week2)

        self.form(data)
        fs = FileSystemStorage()
        with fs.open(FILENAME) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response

    def form(self, data):
        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 0, f'Reporte de Inspecciones', 0, 1, 'C')
        pdf.ln(10)

        for key, ins in enumerate(data):
            index_ins = key + 1
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(185, 10,
                     f'{index_ins}) Tipo: {ins["type_company"].upper()}', 1, 1,)
            if len(ins['companys']) != 0:
                for key_company, company in enumerate(ins['companys']):
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(185, 10,
                            f'  {index_ins}.{key_company+1}) Nombre: {company["name"].upper()}', 1, 1,)

                    pdf.set_font('Arial', 'B', 11)
                    pdf.cell(10, 7, '#', 1, 0, 'C')
                    pdf.cell(45, 7, 'Fecha De Inspección', 1, 0, 'C')
                    pdf.cell(45, 7, 'Proxima Inspección', 1, 0, 'C')
                    pdf.cell(35, 7, 'Resultado', 1, 0, 'C')
                    pdf.cell(50, 7, 'Usuario Responsable', 1, 1, 'C')

                    if len(company['inspections']) != 0:
                        for key_inspections, inspection in enumerate(company['inspections']):
                            info = inspection['fields']
                            result = 'Muy Bueno' if info['result'] == "is_verygood" else 'Bueno' if info[
                                'result'] == "id_good" else 'Malo'
                            pdf.set_font('Arial', '', 11)
                            pdf.cell(10, 7, f'{key_inspections+1}', 1, 0, 'C')
                            pdf.cell(45, 7, f'{info["date"]}', 1, 0, 'C')
                            pdf.cell(45, 7, f'{info["next_date"]}', 1, 0, 'C')
                            pdf.cell(35, 7, f'{result}', 1, 0, 'C')
                            pdf.cell(
                                50, 7, f'{info["account_register"][0]}', 1, 1, 'C')
                            pdf.multi_cell(
                                185, 7, f'Observaciones: {info["notes"]}', 1, 1, '')
                    else:
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(185, 10,
                                f'No Tiene Inspecciones Registradas', 1, 1, 'C')
            else:
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(185, 10, f'No Tiene Compañias Registradas', 1, 1, 'C')
            pdf.ln(10)

        pdf.output(FILENAME, 'F')


class ReportInspectionExpired(View):

    def get(self, *args, **kwargs):
        data = get_inspections_expired()
        self.form(data)
        fs = FileSystemStorage()
        with fs.open(FILENAME) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response

    def form(self, inspections):
        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 0, f'Reporte de Inspecciones Vencidas', 0, 1, 'C')
        pdf.ln(10)
        for i, inspection in enumerate(inspections):
            info = inspection['inspection']['result']
            result = 'Muy Bueno' if info == "is_verygood" else 'Bueno' if info == "is_good" else 'Malo'
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(10, 7, '#', 1, 0, 'C')
            pdf.cell(70, 7, 'TIPO', 1, 0, 'C')
            pdf.cell(105, 7, "NOMBRE", 1, 1, "C")
            pdf.set_font('Arial', '', 12)
            pdf.cell(10, 7, f'{i+1}', 1, 0, "C")
            pdf.cell(70, 7, f'{inspection["type_company"].upper()}', 1, 0, "C")
            pdf.cell(105, 7, f'{inspection["name"].upper()}', 1, 1, "C")
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(40, 7, 'Ultima Inspección', 1, 0, 'C')
            pdf.cell(50, 7, 'Fecha De Vencimiento', 1, 0, 'C')
            pdf.cell(35, 7, "Resultado", 1, 0, "C")
            pdf.cell(60, 7, "Usuario Responsable", 1, 1, "C")
            pdf.set_font('Arial', '', 12)
            pdf.cell(40, 7, f"{inspection['inspection']['date']}", 1, 0, 'C')
            pdf.cell(50, 7, f"{inspection['inspection']['pass_date']}", 1, 0, 'C')
            pdf.cell(35, 7, f'{result}', 1, 0, "C")
            pdf.cell(60, 7, f"{inspection['inspection']['user']}", 1, 1, "C")
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(
                185, 7, f'Observaciones: {inspection["inspection"]["notes"]}', 1, 1, '')
            pdf.ln(10)
        pdf.output(FILENAME, 'F')
