from click import style
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
from peewee import fn, JOIN, Case


from models import DetailPack, Drawing, Faza, Point, PointPart
from qr import QRPack

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))
p_style = ParagraphStyle(name='Normal',fontName='rus',fontSize=10,)

def PackList(pack):
  print(pack)
  page = 1
  pdf = canvas.Canvas(f'media/Пакет {pack.id}.pdf', pagesize=A4)
  pdf.setTitle('')
  tab = []
  index = 1
  details = DetailPack.select().where(DetailPack.pack == pack.id)
  for detail in details:
    names = PointPart.select(PointPart,fn.COUNT(fn.DISTINCT(PointPart.point)).alias('count')).join(Point).join(Drawing).where(PointPart.detail == detail.detail.detail).group_by(PointPart.point,Drawing.id)
    for name in names:
      tab.append([index,name.point.name,name.point.assembly.assembly,detail.detail.detail,'шт.',name.count,float(name.point.assembly.weight),''])
      index += 1
      if index == 37:
        page = 2
        Pdf(pdf,pack,tab,page)
        pdf.showPage()
        tab = []
        page = 3
  Pdf(pdf,pack,tab,page)
  pdf.save()
  return f'media/Пакет {pack.id}.pdf'

def Pdf(pdf,pack,tab,page):
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02]
  heightList = [height*0.015,height*0.96,height*0.025]
  mainTable = Table([
    ['','',''],
    ['',Header(pdf,pack,widthList[1],heightList[1],tab,page),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    # ('GRID',(1,1),(1,1),1,'red'),
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

def Header(pdf,pack,width,height,tab,page):


  if page == 1:
    heightList = [70,20,185,30,len(tab) * 12,60,30,15,height - 410 - (len(tab) * 12)]
    table = Table([
      [Header1(pdf,pack,width,heightList[0])],
      [f'Упаковочный лист № {pack.number}  от  {pack.date}'],
      [Header2(pdf,pack,width,heightList[2])],
      [Body1(width,30)],
      [Body2(tab,pack,width,heightList[4])],
      [Footer1(pack,width,75)],
      [''],
      ['м.п   Упаковал:___________________ Гнебедюк С.Ю'],
      ['']
    ],colWidths=width,
      rowHeights=heightList)
  elif page == 2:
    heightList = [70,20,185,30,len(tab) * 12,60,30,15,height - 410 - (len(tab) * 12)]
    table = Table([
      [Header1(pdf,pack,width,heightList[0])],
      [f'Упаковочный лист № {pack.number}  от  {pack.date}'],
      [Header2(pdf,pack,width,heightList[2])],
      [Body1(width,30)],
      [Body2(tab,pack,width,heightList[4])],
      [''],
      [''],
      [''],
      ['']
    ],colWidths=width,
      rowHeights=heightList)
  elif page == 3:
    heightList = [0,0,0,30,len(tab) * 12,60,30,15,height - 135 - (len(tab) * 12)]
    table = Table([
      [''],
      [''],
      [''],
      [Body1(width,30)],
      [Body2(tab,pack,width,heightList[4])],
      [Footer1(pack,width,75)],
      [''],
      ['м.п   Упаковал:___________________ Гнебедюк С.Ю'],
      ['']
    ],colWidths=width,
      rowHeights=heightList)




  table.setStyle([
    ('GRID',(0,1),(0,1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,1),(0,1),'CENTER'),
    ('ALIGN',(0,-2),(0,-2),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(0,0),0),
    ('VALIGN',(0,0),(0,0),'TOP'),
  ])
  return table

def Header1(pdf,pack,width,height):
  img = Image(QRPack(pack.number),70,height,kind='proportional')
  widthList = [width*0.5,width*0.5]
  table = Table([
    [img,pack.number],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'black'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),50),
    ('FONTSIZE',(0,0),(-1,-1),65),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(1,0),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),

  ])
  return table

def Header2(pdf,pack,width,height):
  widthList = [width*0.4,width*0.6]
  heightList = [25,40,40,40,40]
  table = Table([
    ['Номер договора, спецификации',Paragraph(pack.order.contract,p_style)],
    ['Поставщик (наименование, адрес, ИНН):',Paragraph('ООО «Байкалстальстрой», 666037, Иркутская область, город Шелехов, улица Известковая, дом 2, ИНН 3810061670',p_style)],
    ['Покупатель (наименование, адрес):',Paragraph(pack.order.customer,p_style)],
    ['Грузополучатель (наименование, адрес):',Paragraph(pack.order.consignee,p_style)],
    [Paragraph('Номенклатурное наименование комплектного Оборудования, ТМЦ:',p_style),Paragraph(pack.order.name,p_style)],
  ],colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('ALIGN',(0,0),(0,0),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body1(width,height):
  widthList = [25,115,90,90,60,60,60,width-500]
  table = Table([
    ['№',
    Paragraph('Наименование изделия',p_style),
    Paragraph('Марка изделия',p_style),
    Paragraph('Номер наряда',p_style),
    'Ед.изм.',
    'Кол-во',
    'Вес ед.',
    'Примечание'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body2(tab,pack,width,height):
  widthList = [25,115,90,90,60,60,60,width-500]
  heightList = height/len(tab)
  
  table = Table(tab
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(0,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Footer1(pack,width,height):
  widthList = [105,90]
  heightList = 15
  netto = DetailPack.select(fn.SUM(Faza.weight)).where(DetailPack.pack == pack.id).join(Faza).group_by(DetailPack.pack).scalar()
  table = Table([
    ['',''],
    ['Вид упаковки',pack.pack],
    ['Габариты, мм.',pack.size],
    ['Вес нетто, кг',float(netto)],
    ['Вес брутто, кг',round(float(netto) * 1.005,3)]
  ]
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,1),(-1,-1),1,'black'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(-1,-1),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table