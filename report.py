from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, SimpleDocTemplate

def Pdf():
    c = (0,0,255)
    data = [['1','2','3'],['1','2','3']]
    pdf = canvas.Canvas('My.pdf',bottomup=1)
    # pdf = SimpleDocTemplate('My.pdf')
    pdfmetrics.registerFont(TTFont('rus','Univers.ttf'))
    pdf.setTitle('Title')
    pdf.setStrokeColorRGB(255,255,255)
    pdf.setFillColorRGB(c[0],c[1],c[2])
    pdf.rect(150,790,50,30,fill=1,stroke=0)
    pdf.rect(300,790,50,30,fill=1,stroke=0)
    pdf.setFillColorRGB(255,255,255)
    pdf.setFont('rus',16)
    pdf.drawCentredString(175,800,'Пилы')
    pdf.drawCentredString(325,800,'41')
    pdf.setFillColorRGB(0,0,0)
    pdf.drawString(210,800,'№ 1234')
    pdf.drawString(360,800,'10')

    pdf.save()

    # pdf2 = SimpleDocTemplate('My.pdf')
    
    # table = Table(data)
    # elems = []
    # elems.append(table)
    # elems.append(pdf)

    # pdf2.build(elems)
    
    
    
    
    
    
    # pdf2.save()