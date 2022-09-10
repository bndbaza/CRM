from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
# from models import PointPart, Part, Point
from models import *
from peewee import fn, Case, Cast
from qr import QRAuth, QRRun

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

general = {}

stroka = 12

vid = 'Закладные'

def BaseInfo(details,case):
  info = PointPart.select(PointPart,fn.MAX(Part.length).alias('length')).join(Part).where(PointPart.detail.in_(details),PointPart.weld == 1).group_by(PointPart.detail)
  noweld = []
  for now in PointPart.select().where(PointPart.detail.in_(details),PointPart.weld == 0).group_by(PointPart.detail):
    noweld.append(PointPart.select(PointPart,fn.MAX(Part.length).alias('length'),fn.SUM(Part.count).alias('count')).join(Part).join_from(PointPart,Point).where(PointPart.detail == now.detail,PointPart.weld == 0).group_by(Part.number))
  nowelds = []
  while len(noweld) > 7:
    nowelds.append([noweld.pop(),noweld.pop(),noweld.pop(),noweld.pop(),noweld.pop(),noweld.pop(),noweld.pop()])
  if noweld:
    nowelds.append(noweld)
  bases = []
  d = []
  size = 0
  for i in info:
    b = len(i.part.assembly.parts)*stroka+140
    if (size + b)<= 816 and i == info[-1]:
      d.append(i)
      bases.append(d)
    elif (size + b)> 816 and i == info[-1]:
      bases.append(d)
      bases.append([i])
    elif (size + b)<= 816:
      size += b
      d.append(i)
    else:
      bases.append(d)
      d = [i]
      size = b
    
  try:
    general['case'] = info[0].part.assembly.cas.cas
    general['faza'] = info[0].point.faza
    general['color'] = info[0].part.assembly.cas.color
  except:
    general['case'] = noweld[0][0].part.assembly.cas.cas
    general['faza'] = noweld[0][0].point.faza
    general['color'] = noweld[0][0].part.assembly.cas.color
  return Pdf(bases,nowelds)

def Pdf(bases,nowelds):
  case = general['case']
  faza = general['faza']
  pdf = canvas.Canvas(f'reports/Наряды {case} {faza}.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')
  for base in bases:
    Pdf1(pdf,base=base)
    pdf.showPage()
  if len(nowelds)>0:
    for noweld in nowelds:
      Pdf1(pdf,noweld=noweld)
      pdf.showPage()
  pdf.save()
  return f'reports/Наряды {case} {faza}.pdf'

def Pdf1(pdf,base=0,noweld=0):
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02,]
  heightList = [height*0.015,height*0.97,height*0.015,]
  if noweld:
    vid = Compl(widthList[1],heightList[1],noweld)
  else:
    vid = PrintTab(widthList[1],heightList[1],base)
  mainTable = Table([
    ['','',''],
    ['',vid,''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
  ])
  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)

def PrintTab(width,height,base):
  # print(height*0.07 + 40 + height*0.05)
  lis = []
  heightList = []
  for i in base:
    c2 = (len(i.part.assembly.parts))
    heightList.append(height*0.07)
    heightList.append(8+(c2*12)+32)
    heightList.append(height*0.05)
    lis.append([Header(width,height*0.07,i)])
    lis.append([Body(width,8+(c2*12)+32,i,c2)])
    lis.append([Footer(width,height*0.05,i)])
  heightDown = 0
  for i in heightList:
    heightDown = heightDown + i
  heightList.append(height - heightDown)
  lis.append([''])
  table = Table(lis,colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header(width,height,base):
  widthList = [60,width-60]
  img = Image(QRAuth(base.detail,general['case'],'weld'),widthList[0],height,kind='proportional')
  table = Table([
    [img,Header1(widthList[1],height,base)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header1(width,height,base):
  heightList = [height*0.2,height*0.3,height*0.5]
  table = Table([
    [''],
    [Header2(width,heightList[1],base)],
    ['']
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header2(width,height,base):
  try:
    base.count
    color = 'purple'
    name = 'K'
  except:
    color = 'red'
    name = 'KCW'
  widthList = [width*0.1,width*0.2,width*0.2,width*0.2,width*0.2,width*0.1]
  table = Table([
    [general['faza'],name,'№'+str(base.detail),general['case'],'','']
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(1,0),(1,0),color),
    ('BACKGROUND',(3,0),(3,0),general['color']),
    ('TEXTCOLOR',(1,0),(1,0),'white'),
    ('TEXTCOLOR',(3,0),(3,0),'black'),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ('ALIGN',(0,0),(0,0),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('FONTSIZE',(0,0),(-1,-1),14),
    ('FONTNAME',(0,0),(-1,-1),'rus')
  ])
  return table

def Footer(width,height,base):
  # widthList = [width*0.35,width*0.3,width*0.35]
  widthList = [width*0.05,width*0.9,width*0.05]
  image_run = QRRun(base.detail,general['case'],'weld')
  table = Table([
    # [Footer1(widthList[0],height,image_run,base),Footer5(widthList[1],height),Footer1(widthList[2],height,image_run,base)],
    ['',Footer5(widthList[1],height),''],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(0,0),1,'black'),
    # ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer1(width,height,image,base):
  heightList = [height*0.1,height*0.9]
  table = Table([
    ['Байкалстальстрой     +7(3952)407-203'],
    [Footer2(width,heightList[1],image,base)],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(0,0),'RIGHT'),
    ('VALIGN',(0,0),(0,0),'MIDDLE'),
  ])
  return table

def Footer2(width,height,image,base):
  widthList = [width*0.4,width*0.6]
  table = Table([
    [Footer3(widthList[0],height,base),Footer4(widthList[1],height,image,base)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),10),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('ALIGN',(0,0),(0,0),'RIGHT'),
    # ('VALIGN',(0,0),(0,0),'MIDDLE'),
  ])
  return table

def Footer3(width,height,base):
  heightList = height/5
  try:
    length = base.length
  except:
    length = base.part.length
  table = Table([
    ['наряд '+str(base.detail)],
    ['длина ст. '+str(int(length))],
    ['вес '+str(float(base.part.assembly.weight))],
    ['заказ '+general['case']],
    ['фаза '+str(general['faza'])],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,1),(-1,-1),10),
    ('FONTSIZE',(0,0),(0,0),18),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('ALIGN',(0,0),(0,0),'RIGHT'),
    ('VALIGN',(0,0),(0,0),'MIDDLE'),
  ])
  return table

def Footer4(width,height,image,base):
  heightList = [height*0.6,height*0.4]
  img = Image(image,width,heightList[0],kind='proportional')
  table = Table([
    [img],
    [base.part.assembly.assembly],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTSIZE',(0,0),(-1,-1),30),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
  ])
  return table

def Footer5(width,height):
  # heightList = [height*0.6,height*0.4]
  heightList = height/2
  widthList = width/2
  table = Table([
    ['Комплектовщик_______________','Сборщик_____________________'],
    ['Сварщик_____________________','Маляр_______________________'],
  ],colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('TOPPADDING',(0,0),(-1,-1),0),
    # ('FONTSIZE',(0,0),(-1,-1),30),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
  ])
  return table

def Body(width,height,base,row):
  heightList = [20]
  heightList.append(row*stroka)
  heightList.append(height-20-(row*stroka))


  table = Table([
    [Body1(heightList[0],base)],
    [Body2(width,heightList[1],base,row)],
    [''],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('ROTATE',(0,0),(0,0),90),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
  ])
  return table

def Body1(height,base):
  try:
    if base.point.name == vid:
      widthList = [50,85,30,30,50,135,60,55,75]
      table_list = ['Марка','Чертеж','Сбор.№','№','Кол.','Профиль','Длина','Вес','Марка стали']
    else:
      widthList = [60,35,55,45,50,135,60,55,75]
      table_list = ['Конструкция','Марка','Чертеж','№','Кол.','Профиль','Длина','Вес','Марка стали']
  except:
    widthList = [60,35,55,45,50,135,60,55,75]
    table_list = ['Конструкция','Марка','Чертеж','№','Кол.','Профиль','Длина','Вес','Марка стали']
  table = Table([table_list]
  ,colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),8),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table


def Body2(width,height,base,row):
  try:
    if base.point.name == vid:
      widthList = [50,85,30,30,50,135,60,55,75]
    else:
      widthList = [60,35,55,45,50,135,60,55,75]
  except:
    widthList = [60,35,55,45,50,135,60,55,75]

  heightList = height/row
  mas = []
  try:
    base[0].count
    for i in base:
      x = ''
      if i.part.width != None and i.part.width !='': x='x'
      if i.point.name == vid:
        mas.append((i.point.name,i.point.assembly.assembly,i.point.draw,f'{i.part.number}({i.part.sn})',i.count,i.part.profile+' '+i.part.size+x+i.part.width,int(i.part.length),float(i.part.weight),i.part.mark))
      else:
        mas.append((i.point.name,i.point.assembly.assembly,i.point.draw,i.part.number,i.count,i.part.profile+' '+i.part.size+x+i.part.width,int(i.part.length),float(i.part.weight),i.part.mark))
  except:
    for i in base.part.assembly.parts:
      x = ''
      if i.width != None and i.width !='': x='x'
      if base.point.name == vid:
        mas.append((base.point.assembly.assembly,base.point.draw,i.sn,i.number,i.count,i.profile+' '+i.size+x+i.width,int(i.length),float(i.weight),i.mark))
      else:
        mas.append((base.point.name,base.point.assembly.assembly,base.point.draw,i.number,i.count,i.profile+' '+i.size+x+i.width,int(i.length),float(i.weight),i.mark))

  table = Table(mas
  ,colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),8),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Compl(width,height,nowelds):
  # import math
  # x=0
  # for i in noweld:
  #   x += i.count
  # x = math.ceil(x/3)
  lis = []
  heightList = []
  for noweld in nowelds:
    c2 = len(noweld)
    heightList.append(height*0.07)
    heightList.append(8+(c2*12)+32)
    # heightList.append(height*0.15*x)
    # heightList.append(height*0.05)
    lis.append([Header(width,height*0.07,noweld[0])])
    lis.append([Body(width,8+(c2*12)+32,noweld,c2)])
    # lis.append([FooterCompl(width,height*0.05,noweld)])
  table = Table(lis,colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table


def FooterCompl(width,height,bases):
  widthList = [width/3,width/3,width/3]
  noweld = PointPart.select().where(PointPart.detail == bases[0].detail)
  image_run = QRRun(bases[0].detail,general['case'],'weld')
  tab = []
  d = []
  for base in noweld:
    if len(d) < 3 and base == noweld[-1]:
      d.append(Footer1(widthList[0],height,image_run,base))
      tab.append(d)
    elif len(d) < 3:
      d.append(Footer1(widthList[0],height,image_run,base))
    else:
      tab.append(d)
      d = [Footer1(widthList[0],height,image_run,base)]
  table = Table([''],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table