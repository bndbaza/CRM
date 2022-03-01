from pymysql import NULL
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from models import PointPart, Point, Drawing, Order, Part
from peewee import fn, Case

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

def Pdf(list,faza,case):
  pdf = canvas.Canvas(str(list[0][0])+'list.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02,]
  heightList = [height*0.015,height*0.05,height*0.02,height*0.9,height*0.015,]
  mainTable = Table([
    ['','',''],
    ['','Заказ '+case+' Фаза '+str(faza),''],
    ['',Head(widthList[1],heightList[2]),''],
    ['',Column(list,widthList[1],heightList[3]),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
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
  pdf.showPage()
  pdf.save()

def Head(width,height):
  table = Table([
    ['Наряд','Пм','Пб','Сп','Ф','Сф','скос','вырез','фаска','F','гибка','сборка','W','M']
  ],colWidths=width/14,rowHeights=height)
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


def Column(list,width,height):
  table = Table(list,colWidths=width/14,rowHeights=height/len(list))
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('FONTSIZE',(0,0),(-1,-1),7),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table
  

def Inf_list(faza,case):

  list = []
  for l in PointPart.select(PointPart.detail,
                            fn.COUNT(Case(None,[(Part.work == 'saw_s',1)], None)).alias('saw_s'),
                            fn.COUNT(Case(None,[(Part.work == 'saw_b',1)], None)).alias('saw_b'),
                            fn.COUNT(Case(None,[(Part.work == 'cgm',1)], None)).alias('cgm'),
                            fn.SUM(Case(None, [((PointPart.hole == 1) & (Part.size.cast('int') >= 14) & (PointPart.cgm == 1),1)], 0)).alias('hole_cgm'),
                            fn.SUM(Case(None, [((PointPart.hole == 1) & (PointPart.saw == 1),1)], 0)).alias('hole_saw'),
                            fn.SUM(PointPart.bevel).alias('bevel'),
                            fn.SUM(PointPart.notch).alias('notch'),
                            fn.SUM(PointPart.chamfer).alias('chamfer'),
                            fn.SUM(PointPart.milling).alias('milling'),
                            fn.SUM(PointPart.bend).alias('bend'),
                            fn.SUM(PointPart.weld).alias('weld'),
                            ).join(Point).join(Drawing).join(Order).join_from(PointPart,Part).where(Point.faza == faza,Order.cas == case).group_by(PointPart.detail):
    lis = []
    lis.append(l.detail)
    if l.saw_s > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.saw_b > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.hole_saw > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.cgm > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.hole_cgm > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.bevel > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.notch > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.chamfer > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.milling > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.bend > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.weld > 0:
      lis.append('+')
    else:
      lis.append('')
    if l.weld > 0:
      lis.append('+')
    else:
      lis.append('')
    lis.append('+')
    list.append(lis)
  print(len(list))
  list1 = []
  y = 0
  z = 0
  for i in list:
    y += 1
    z += 1
    if y > 50:
      list1.append(i)
  Pdf(list1,faza,case)

        



def Inf_calc(cal):
  inf = (len(cal)//3)
  y = []
  z = []
  for i in cal:
    z.append([i.detail])
    if len(z) == inf and len(y) < 2:
      y.append(z)
      z = []
    elif len(z) == inf and len(y) >= 2:
      y.append(z)
  return y