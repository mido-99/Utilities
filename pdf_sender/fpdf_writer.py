from fpdf import FPDF

output = 'output.pdf'

pdf = FPDF(orientation='p', unit='pt')
pdf.add_page()
pdf.set_font("Times", size = 12)
pdf.set_xy(60, 75)

with open('cont_1.txt', 'r', encoding='latin-1') as file:
    for x in file:
        pdf.set_x(60)
        pdf.cell(200, 14, x, ln=1, align='L')

pdf.output(output)
