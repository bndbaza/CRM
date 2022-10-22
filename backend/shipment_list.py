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
import datetime


from models import DetailPack, Drawing, Faza, Point, PointPart, Shipment
from qr import QRPack, QRShip

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))
p_style = ParagraphStyle(name='Normal',fontName='rus',fontSize=9,)
end = {'page':1,'finish':False}

hstr = 12

def ShipmentList(id):
  pdf = canvas.Canvas(f'media/Машина {id}.pdf', pagesize=A4)
  pdf.setTitle('')
  tab = {'count':0,'tab':[],'wight':0}
  index = 1
  ship = Shipment.select().where(Shipment.id == id).first()
  for pack in ship.packeds:
    count = 0
    for det in pack.detailpacks:
      count += len(PointPart.select(PointPart,fn.COUNT(fn.DISTINCT(PointPart.point)).alias('count')).join(Point).join(Drawing).where(PointPart.detail == det.detail.detail).group_by(PointPart.detail,Drawing.id))
    if tab['count'] == 0 and count > 50 and end['page'] == 1:
      pass
    elif tab['count'] + count > 40 and end['page'] == 1:
      Pdf(pdf,ship,tab)
      pdf.showPage()
      tab['count'] = 0
      tab['tab'] = []
      end['page'] += 1
    elif tab['count'] + count > 50 and end['page'] != 1:
      Pdf(pdf,ship,tab)
      pdf.showPage()
      tab['count'] = 0
      tab['tab'] = []
      end['page'] += 1
    dic = {'pack':[pack.number,pack.size,pack.pack],'detail':[]}
    for detail in pack.detailpacks:
      names = PointPart.select(PointPart,fn.COUNT(fn.DISTINCT(PointPart.point)).alias('count')).join(Point).join(Drawing).where(PointPart.detail == detail.detail.detail).group_by(PointPart.detail,Drawing.id)
      for name in names:
        tab['wight'] += name.count * float(name.point.assembly.weight)
        dic['detail'].append([index,name.point.name,name.point.assembly.assembly,detail.detail.detail,'шт.',name.count,float(name.point.assembly.weight)])
        if float(detail.detail.weight) != name.count * float(name.point.assembly.weight):
          print(detail.detail.detail,detail.detail.weight,name.count * float(name.point.assembly.weight))
        index += 1
      if len(dic['detail']) >= 40 and end['page'] == 1:
        tab['count'] += len(dic['detail'])
        tab['tab'].append(dic)
        Pdf(pdf,ship,tab)
        dic['detail'] = []
        pdf.showPage()
        tab['count'] = 0
        tab['tab'] = []
        end['page'] += 1
      elif len(dic['detail']) >= 50:
        tab['count'] += len(dic['detail'])
        tab['tab'].append(dic)
        Pdf(pdf,ship,tab)
        dic['detail'] = []
        pdf.showPage()
        tab['count'] = 0
        tab['tab'] = []
        end['page'] += 1
    tab['count'] += len(dic['detail'])
    tab['tab'].append(dic)
    dic = []
  end['finish'] = True
  print
  Pdf(pdf,ship,tab)
  pdf.save()
  end['page'] = 1
  end['finish'] = False
  return f'media/Машина {id}.pdf'

def Pdf(pdf,id,tab):
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02]
  heightList = [height*0.015,height*0.96,height*0.025]
  mainTable = Table([
    ['','',''],
    ['',Header(tab,pdf,id,widthList[1],heightList[1]),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),20),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)

def Header(tab,pdf,ship,width,height):
  index = 1
  heightList = [70,15,145,25,tab['count'] * hstr,15,60,30,15,height - 380 - tab['count'] * hstr]
  ship.date = datetime.datetime.today()
  ship.save()
  if end['finish'] == True and end['page'] == 1:
    table = Table([
      [Header1(pdf,ship,width,heightList[0])],
      [f'Комплектовочная ведомость № {ship.number}  от  {ship.date}'],
      [Header2(pdf,ship,width,heightList[2])],
      [Body1(width,25)],
      [Body2(tab,width,heightList[4])],
      [],
      [Footer1(tab,width,75)],
      [''],
      [''],
      # ['Комплектовщик:___________________ Гнебедюк С.Ю'],
      ['']
    ],colWidths=width,
      rowHeights=heightList)

  elif end['finish'] == False and end['page'] == 1:
    table = Table([
      [Header1(pdf,ship,width,heightList[0])],
      [f'Комплектовочная ведомость № {ship.number}  от  {ship.date}'],
      [Header2(pdf,ship,width,heightList[2])],
      [Body1(width,25)],
      [Body2(tab,width,heightList[4])],
      [''],
      [''],
      [''],
      ['']
    ],colWidths=width,
      rowHeights=heightList)

  elif end['finish'] == True and end['page'] != 1:
    heightList = [0,0,0,25,tab['count'] * hstr,15,60,30,15,height - 220 - tab['count'] * hstr]
    table = Table([
      [''],
      [''],
      [''],
      [Body1(width,25)],
      [Body2(tab,width,heightList[4])],
      [],
      [Footer1(tab,width,75)],
      [''],
      [''],
      # ['Комплектовщик:___________________ Гнебедюк С.Ю'],
      ['']
    ],colWidths=width,
      rowHeights=heightList)

  elif end['finish'] == False and end['page'] != 1:
    heightList = [0,0,0,25,tab['count'] * hstr,60,30,hstr,height - 130 - tab['count'] * hstr]
    table = Table([
      [''],
      [''],
      [''],
      [Body1(width,25)],
      [Body2(tab,width,heightList[4])],
      [''],
      [''],
      [''],
      ['']
    ],colWidths=width,
      rowHeights=heightList)

  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,1),(0,1),'CENTER'),
    ('ALIGN',(0,-2),(0,-2),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(0,0),0),
    ('VALIGN',(0,0),(0,0),'TOP'),
  ])
  return table

def Header1(pdf,pack,width,height):
  img = Image(QRShip(pack.number),70,height,kind='proportional')
  widthList = [width*0.5,width*0.5]
  table = Table([
    [img,pack.number],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
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
  heightList = [25,25,15,35,25,20]
  table = Table([
    ['Номер договора, спецификации',Paragraph(pack.order.contract,p_style)],
    ['Поставщик (наименование, адрес, ИНН):',Paragraph('ООО «Байкалстальстрой», 666037, Иркутская область, город Шелехов, улица Известковая, дом 2, ИНН 3810061670',p_style)],
    ['Покупатель (наименование, адрес):',Paragraph(pack.order.customer,p_style)],
    ['Грузополучатель (наименование, адрес):',Paragraph(pack.order.consignee,p_style)],
    ['Номенклатурное наименование:',Paragraph(pack.order.name,p_style)],
    ['Вид и номер транспортного средства:',Paragraph(pack.car+', '+pack.number_car,p_style)],
  ],colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body1(width,height):
  widthList = [25,95,79,57,47,31.5,50,57,75,55]
  table = Table([
    ['№',
    Paragraph('Наименование изделия',p_style),
    Paragraph('Марка изделия',p_style),
    Paragraph('Номер наряда',p_style),
    Paragraph('Ед. изм.',p_style),
    'Кол.',
    'Вес',
    Paragraph('Упаковочный лист',p_style),
    Paragraph('Габариты, мм.',p_style),
    Paragraph('Вид упаковки',p_style)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table


def fake(height=15):
  widthList = [25,95,79,57,47,31.5,50,57,75,55]
  table = Table([
    ['41',
    'Метизы',
    '',
    '',
    'кг.',
    '',
    '1514.48',
    '',
    '',
    'Ящик'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(-1,-1),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table









def Body2(tab,width,height):
  widthList = [384.5,187]
  heightList = []
  tabl = []
  for t in tab['tab']:
    tabl.append([Body3(t['detail'],widthList[0],hstr * len(t['detail'])),Body4(t['pack'],widthList[1],hstr * len(t['detail']))])
    heightList.append(hstr * len(t['detail']))
  table = Table(
    tabl
  
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table


def Body3(tab,width,height):
  widthList = [25,95,79,57,47,31.5,50]
  heightList = height / len(tab)
  table = Table(
    tab
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(0,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body4(tab,width,height):
  widthList = [57,75,55]
  heightList = height
  table = Table(
    [tab]
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table


def Footer1(tab,width,height):
  widthList = [105,90,width - 105 - 90]
  heightList = 15
  table = Table([
    ['Вес нетто, кг',round(tab['wight'],1),'Комплектовщик:___________________ Гнебедюк С.Ю'],
  ]
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,1),(-2,-1),1,'black'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(-1,-1),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table