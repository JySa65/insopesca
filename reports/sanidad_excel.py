from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment, Border, Side
from django.views.generic import View
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

FILENAME = f'{settings.MEDIA_ROOT}/reports_excel.xlsx'

class InpectionsCompany(View):
    def get(self, request, *args, **kwargs):
        return self.form()
        # fs = FileSystemStorage()
        # with fs.open(FILENAME) as xlsx:
        #     response = HttpResponse(xlsx)
        #     response['Content-type'] = 'application/ms-excel'
        #     response['Content-Disposition'] = 'inline; filename="reporte_excel.xlsx"'
        # return response

    def form(self):
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

        wb.save(FILENAME)
        return HttpResponse("si")
