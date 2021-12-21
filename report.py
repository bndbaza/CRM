from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def Pdf():
  pdf = canvas.Canvas('My.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')

  width, height = A4

  mainTable = Table([
    ['QR-code','Pr','PILI','#7123','41','10','P C W M'],
    ['QR-code','Pr','PILI','#7123','41','10','P C W M'],
  ],colWidths=[width*0.2,width*0.1,width*0.2,width*0.1,width*0.1,width*0.1,width*0.2],
    rowHeights=30)

  mainTable.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('BACKGROUND',(2,0),(2,0),colors.blue),
    ('BACKGROUND',(4,0),(4,0),colors.green),
    ('TEXTCOLOR',(2,0),(2,0),'white'),
    ('TEXTCOLOR',(4,0),(4,0),'white'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])

  mainTable.wrapOn(pdf,0,780)
  mainTable.drawOn(pdf,0,780)

  pdf.showPage()
  pdf.save()