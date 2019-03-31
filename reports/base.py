from fpdf import FPDF
from datetime import datetime

FILENAME = 'reports.pdf'

class PDF(FPDF):
    def header(self):
        # self.image(
        #     'static/assets/images/banner.jpeg', 10, 5, 150, 25,)
        self.image(
            'static/assets/images/logo1.png', 160, 5, 30, 25)
        self.set_font('Arial', 'B', 15)
        self.cell(70,5, 'No se qie colcar aqui mientas espere a', 0,1)
        self.cell(70,5, 'volver a preguntar :\'c')
        self.cell(80)
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'B', 8)
        self.cell(8,10,
                  f"Fecha: {str(datetime.now().strftime('%d:%m:%Y'))} a las {str(datetime.now().strftime('%I:%M:%S %p'))}")
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) +
                  ' / {nb}', 0, 0, 'R')
