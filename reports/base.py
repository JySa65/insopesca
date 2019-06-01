from fpdf import FPDF
from datetime import datetime
from django.conf import settings

FILENAME = f'{settings.MEDIA_ROOT}/reports.pdf'

class PDF(FPDF):
    def header(self):
        self.image(
            'static/assets/images/cintillo.png', 5, 5, 200, 25)
        self.image(
            'static/assets/images/logo1.png', 155, 5, 25, 25)
        # self.cell(80)
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'B', 8)
        self.cell(8,10,
                  f"Fecha: {str(datetime.now().strftime('%d:%m:%Y'))} a las {str(datetime.now().strftime('%I:%M:%S %p'))}")
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) +
                  ' / {nb}', 0, 0, 'R')

class PDFL(FPDF):
    def header(self):
        self.image(
            'static/assets/images/cintillo.png', 5, 5, 285, 25)
        self.image(
            'static/assets/images/logo1.png', 225, 5, 25, 25)
        self.ln(30)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'B', 8)
        self.cell(8,10,
                  f"Fecha: {str(datetime.now().strftime('%d:%m:%Y'))} a las {str(datetime.now().strftime('%I:%M:%S %p'))}")
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) +
                  ' / {nb}', 0, 0, 'R')
