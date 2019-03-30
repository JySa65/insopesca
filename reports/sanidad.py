from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from reports.base import PDF
import sys

class ReportSanidadListInpections(View):

    def get(self, *args, **kwargs):
        pdf = PDF('P', 'mm', 'A4')
        pdf.alias_nb_pages()
        # pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Hello World!')
        pdf.cell(40, 10, 'Hello World!')
        pdf.cell(40, 10, 'Hello World!')
        pdf.cell(40, 10, 'Hello World!')
        filename = 'biblioteca.pdf'
        pdf.output(filename, 'F')
        fs = FileSystemStorage()
        with fs.open(filename) as pdf:
            response = HttpResponse(pdf)
            response['Content-type'] = 'application/pdf'
            response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
        return response


