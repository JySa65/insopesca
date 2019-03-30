from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # self.image('static/homepage/images/logo.jpg', 10, 5, 270, 25,)
        self.set_font('Arial', 'B', 15)
        self.cell(80)
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'B', 8)
        # self.cell(8,10,"A las")
        # self.cell(10,10,str(datetime.now().strftime('%I:%M:%S %p')))
        self.cell(0, 10, 'Pagina ' + str(self.page_no()) +
                  ' / {nb}', 0, 0, 'R')
