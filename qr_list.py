from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from models import Worker
from qr import QRUser

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))
color = {
  'weld':('black','white'),
  'assembly':('red','black'),
  'saw':('blue','white'),
  'hole':('green','white'),
  'cgm':('yellow','black'),
  'bend':('grey','black'),
  'milling':('brown','white'),
  'turning':('white','black'),
  'bevel':('orange','black'),
  'notch':('white','black'),
  'point':('pink','black'),
  'chamfer':('violet','black')
}


def QR_pdf():
  pdf = canvas.Canvas('qr.pdf', pagesize=A4)
  pdf.setTitle('')
  user = Worker.select()#.where(Worker.id.in_([77,78]))
  d = []
  y = 1
  z = 1
  for i in user:
    d.append(i)
    if y == 16 or z == len(user):
      QR_pdf1(pdf,d)
      pdf.showPage()
      d = []
      y = 1
    else:
      y += 1
    z += 1
  # pdf.showPage()
  pdf.save()

def QR_pdf1(pdf,user):
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02]
  heightList = [height*0.015,height*0.96,height*0.025,]
  mainTable = Table([
    ['','',''],
    ['',Job(widthList[1],heightList[1],user),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    # ('GRID',(1,1),(-2,-2),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),20),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('BACKGROUND',(2,1),(2,1),colors.green),
    # ('BACKGROUND',(1,1),(1,1),list[y]['color']),
    # ('TEXTCOLOR',(1,1),(2,1),list[y]['color_text']),
  ])
  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)

def Job(width,height,user):
  d = []
  db = []
  
  y = 1
  z = 1
  for i in user:
    d.append(Job1(i,width*0.25,height*0.25))
    if z == len(user):
      db.append(d)
      break
    if y == 4:
      db.append(d)
      d = []
      y = 0
    y += 1
    z += 1
  table = Table(db,
  colWidths=width/4,rowHeights=height/4)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('FONTSIZE',(0,0),(-1,-1),16),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Job1(list,width,height):
  heightList = [height*0.2,height*0.2,height*0.2,height*0.4]
  img = Image(QRUser(list),heightList[3],height,kind='proportional')
  table = Table([
    [list.oper_rus],
    [list.user.surname +' '+ list.user.name +' '+ list.user.patronymic],
    [''],
    [img]


  ],colWidths=width,rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),14),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('BACKGROUND',(0,0),(0,0),color[list.oper][0]),
    ('TEXTCOLOR',(0,0),(0,0),color[list.oper][1]),
  ])
  return table