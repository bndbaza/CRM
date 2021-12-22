from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont('rus','Univers.ttf'))

def Pdf():
  pdf = canvas.Canvas('My.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')

  width, height = A4

  heightList = [height*0.1,height*0.25,height*0.15,height*0.1,height*0.25,height*0.15]

  mainTable = Table([
    [Header1(600,heightList[0])],
    [''],
    [Footer(width,heightList[2])],
    [Header1(600,heightList[0])],
    [''],
    [Footer(width,heightList[2])]
  ],colWidths=width,
    rowHeights=heightList)

  mainTable.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    
  ])

  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)

  pdf.showPage()
  pdf.save()

def Header1(width,height):
  widthList = [width*0.15,width*0.85]
  img = Image('qr-code.gif',widthList[0],height)
  table = Table([
    [img,Header2(widthList[1],height)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(0,0),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header2(width,height):
  heightList = [height*0.2,height*0.3,height*0.5]
  table = Table([
    [''],
    [Header3(width,heightList[1])],
    ['']
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header3(width,height):
  widthList = [width*0.1,width*0.2,width*0.2,width*0.2,width*0.1,width*0.2]
  table = Table([
    ['Пр','ПИЛЫ','№7123','41','10','P C W M'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(1,0),(1,0),colors.blue),
    ('BACKGROUND',(3,0),(3,0),colors.green),
    ('TEXTCOLOR',(1,0),(1,0),'white'),
    ('TEXTCOLOR',(3,0),(3,0),'white'),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ('ALIGN',(0,0),(0,0),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('FONTSIZE',(0,0),(-1,-1),14),
    ('FONTNAME',(0,0),(-1,-1),'rus')
  ])
  return table

def Footer(width,height):
  widthList = [width*0.4,width*0.2,width*0.4]
  table = Table([
    [Footer1(widthList[0],height),'2',Footer1(widthList[0],height)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer1(width,height):
  heightList = [height*0.1,height*0.5,height*0.1,height*0.3]
  table = Table([
    [Footer2(width,heightList[0])],
    [Footer3(width,heightList[1])],
    [Footer4(width,heightList[2])],
    [Footer5(width,heightList[3])]
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer2(width,height):
  widthList = [width*0.1,width*0.8,width*0.1]
  table = Table([
    [10,'Бегунок','П'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Footer3(width,height):
  # widthList = [width*0.1,width*0.8,width*0.1]
  table = Table([
    ['7123'],
  ],colWidths=width,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),65),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('FONTSIZE',(0,0),(-1,-1),60),
  ])
  return table

def Footer4(width,height):
  widthList = [width*0.5,width*0.5]
  table = Table([
    ['П2-2','П С W M'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(-1,-1),(-1,-1),'RIGHT'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('FONTSIZE',(0,0),(-1,-1),60),
  ])
  return table

def Footer5(width,height):
  widthList = [width*0.25,width*0.5,width*0.1,width*0.15]
  table = Table([
    [1,2,3,4],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('ALIGN',(-1,-1),(-1,-1),'RIGHT'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('FONTSIZE',(0,0),(-1,-1),60),
  ])
  return table