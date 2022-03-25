from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from models import *
from peewee import fn, Case, Cast
from qr import QRAuth, QRRun, Delpng
import math

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

def Pdf(infs):
  string = infs[0]['case'].split('/')
  if len(string) > 1:
    string = string[0] + '.' + string[1]
  else:
    string = string[0]
  pdf = canvas.Canvas(string+ ' ' +str(infs[0]['faza'])+'.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')
  lis = []
  for inf in infs:
    if inf['saw_s']['tabl_sum']['table_count'] != None:
      lis.append(('saw_s',inf))
    if inf['saw_b']['tabl_sum']['table_count'] != None:
      lis.append(('saw_b',inf))
    if inf['weld']['tabl'] != None:
      lis.append(('weld',inf))
    if inf['paint']['tabl'] != None:
      lis.append(('paint',inf))
    if inf['cgm']['tabl_sum']['table_count'] != None:
      lis.append(('cgm',inf))
  lis2 = []
  count = 0
  inf=infs
  for i in lis:
    if i[0] != 'weld' and i[0] != 'paint':
      count += len(i[1][i[0]]['tabl'])
    else:
      count += 1
    if count <= 15 and len(lis2) < 3:
      lis2.append(i)
    elif count <= 32 and len(lis2) < 2:
      lis2.append(i)
    else:
      Pdf1(inf,pdf,lis2)
      pdf.showPage()
      if i[0] != 'weld' and i[0] != 'paint':
        count = len(i[1][i[0]]['tabl'])
      else:
        count = 1
      lis2 = []
      lis2.append(i)
  Pdf1(inf,pdf,lis2)
  pdf.save()
  Delpng()



def Pdf1(inf,pdf,lis):
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02,]
  heightList = [height*0.015,height*0.97,height*0.015,]
  mainTable = Table([
    ['','',''],
    ['',PrintTab(widthList[1],heightList[1],inf,lis),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
  ])
  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)


def PrintTab(width,height,inf,lis):
  lis2 = []
  heightList = []
  for i in lis:
    c2 = 1
    if i[0] != 'weld' and i[0] != 'paint':
      c2 = (len(i[1][i[0]]['tabl']))
    if i[0] == 'paint' and i[1]['weld']['tabl'] == None:
      c2 = (len(i[1][i[0]]['tabl2']))
    heightList.append(height*0.07)
    heightList.append(8+(c2*12)+32)
    heightList.append(height*0.15)
    lis2.append([Header1(width,height*0.07,i[1],i[0])])
    lis2.append([Body(width,8+(c2*12)+32,i[1],i[0])])
    lis2.append([Footer(width,height*0.15,i[1],i[0])])
  heightDown = 0
  for i in heightList:
    heightDown = heightDown + i
  heightList.append(height - heightDown)
  lis2.append([''])
  table = Table(lis2,colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table


def Header1(width,height,inf,oper):
  widthList = [60,width-60]
  img = Image(QRAuth(inf['detail'],inf['case'],oper),widthList[0],height,kind='proportional')
  table = Table([
    [img,Header2(widthList[1],height,inf,oper)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header2(width,height,inf,oper):
  heightList = [height*0.2,height*0.3,height*0.5]
  table = Table([
    [''],
    [Header3(width,heightList[1],inf,oper)],
    ['']
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header3(width,height,inf,oper):
  widthList = [width*0.05,width*0.2,width*0.15,width*0.15,width*0.1,width*0.35]
  table = Table([
    [inf['name'][0],inf[oper]['name'],'№'+str(inf['detail']),inf['case'],inf['faza'],inf['work']],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(1,0),(1,0),inf[oper]['color']),
    ('BACKGROUND',(3,0),(3,0),inf['color']),
    ('TEXTCOLOR',(1,0),(1,0),inf[oper]['color_t']),
    ('TEXTCOLOR',(3,0),(3,0),'white'),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ('ALIGN',(0,0),(0,0),'RIGHT'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('FONTSIZE',(0,0),(-1,-1),14),
    ('FONTNAME',(0,0),(-1,-1),'rus')
  ])
  return table

def Footer(width,height,inf,oper):
  widthList = [width*0.35,width*0.3,width*0.35]
  image_run = QRRun(inf['detail'],inf['case'],oper)
  image_aut = QRAuth(inf['detail'],inf['case'],oper)
  table = Table([
    [Footer1(widthList[0],height,'Бегунок',image_run,inf,oper),Footer7(widthList[0],height,inf,oper),Footer1(widthList[0],height,'Авторизация',image_aut,inf,oper)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(0,0),1,'black'),
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer1(width,height,str,image,inf,oper):
  heightList = [height*0.1,height*0.5,height*0.1,height*0.3]
  table = Table([
    [Footer2(width,heightList[0],str,inf,oper)],
    [Footer3(width,heightList[1],inf)],
    [Footer4(width,heightList[2],inf,oper)],
    [Footer5(width,heightList[3],image,inf,oper)],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer2(width,height,str,inf,oper):
  abbreviation = {'ПИЛЫ М':'Пм','ПИЛЫ Б':'Пб','Сборка':'С','ФАСОНКА':'Ф','Малярка':'М'}
  widthList = [width*0.1,width*0.8,width*0.1]
  table = Table([
    [inf['faza'],str,abbreviation[inf[oper]['name']]],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,0),0),
    ('BACKGROUND',(-1,-1),(-1,-1),inf[oper]['color']),
    ('TEXTCOLOR',(-1,-1),(-1,-1),inf[oper]['color_t']),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Footer3(width,height,inf):
  table = Table([
    [inf['detail']],
  ],colWidths=width,
    rowHeights=height)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),65),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('FONTSIZE',(0,0),(-1,-1),60),
  ])
  return table

def Footer4(width,height,inf,oper):
  widthList = [width*0.5,width*0.5]
  table = Table([
    [inf['mark'],inf['work']],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(-1,-1),(-1,-1),'RIGHT'),
  ])
  return table

def Footer5(width,height,image,inf,oper):
  widthList = [width*0.25,width*0.4,width*0.1,width*0.25]
  img = Image(image,widthList[1],height,kind='proportional')
  table = Table([
    [Footer6(widthList[0],height,inf,oper),img,inf['name'][0],inf['case']],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(0,0),1,'black'),
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,0),0),
    ('BOTTOMPADDING',(0,0),(-1,0),0),
    ('TOPPADDING',(0,0),(-1,0),0),
    ('RIGHTPADDING',(0,0),(-1,0),0),
    ('BACKGROUND',(-1,0),(-1,0),inf['color']),
    ('TEXTCOLOR',(-1,0),(-1,0),'white'),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(-1,0),'CENTER'),
    ('VALIGN',(1,0),(-1,0),'MIDDLE'),
    ('FONTSIZE',(2,0),(2,0),16),
    ('FONTSIZE',(3,0),(3,0),14),
  ])
  return table


def Footer6(width,height,inf,oper):
  heightList = [height/3,height/3,height/3]
  i = inf['master'].part.size
  if oper != 'weld' and oper != 'paint':
    table_list = [[i],[inf[oper]['tabl_sum']['table_count']],[float(inf[oper]['tabl_sum']['table_weight'])]]
  else:
    table_list = [[i],[1],[float(inf[oper]['tabl'].part.assembly.weight)]]
  table = Table(table_list,colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
  ])
  return table

def Footer7(width,height,inf,oper):
  if oper == 'saw_s' or oper == 'saw_b':
    heightList = []
    tabl = [['Пилы _______________________']]
    if 'Сп' in inf['work']:
      tabl.append(['Сверловка __________________'])
    for i in range(len(tabl)):
      heightList.append(height/len(tabl))
  elif oper == 'weld':
    heightList = []
    tabl = [['Сборка _____________________']]
    if 'W' in inf['work']:
      tabl.append(['Сварка _____________________'])
    for i in range(len(tabl)):
      heightList.append(height/len(tabl))
  elif oper == 'paint':
    heightList = []
    tabl = [['Маляр ______________________']]
    # if 'W' in inf['work']:
    #   tabl.append(['Сварка _____________________'])
    for i in range(len(tabl)):
      heightList.append(height/len(tabl))
  else:
    heightList = []
    tabl = [['ЦГМ ________________________']]
    tabl.append(['Зачистка ___________________'])
    tabl.append(['Правка _____________________'])
    if 'Сф' in inf['work']:
      tabl.append(['Сверловка __________________'])
    for i in range(len(tabl)):
      heightList.append(height/len(tabl))
  table = Table(tabl
  ,colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
  ])
  return table

def Body(width,height,inf,oper):
  heightList = [20]
  if oper != 'weld' and oper != 'paint':
    heightList.append(len(inf[oper]['tabl'])*12)
    heightList.append(12)
    heightList.append(height-20-12-(len(inf[oper]['tabl']*12)))
  elif inf['weld']['tabl'] == None and oper == 'paint':
    heightList.append(len(inf[oper]['tabl2'])*12)
    heightList.append(12)
    heightList.append(height-20-12-(len(inf[oper]['tabl2']*12)))
  else:
    heightList.append(12)
    heightList.append(12)
    heightList.append(height-20-12-12)


  table = Table([
    [Body1(width,heightList[0],inf,oper)],
    [Body2(width,heightList[1],inf,oper)],
    [Body3(width,heightList[2],inf,oper)],
    [''],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('ROTATE',(0,0),(0,0),90),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
  ])
  return table

def Body1(width,height,inf,oper):
  if oper != 'weld' and oper != 'paint':
    widthList = [60,35,30,20,25,110,35,30,50,25,25,25,25,25,25,25]
    table_list = ['Конструкция','Марка','Чертеж','№','Кол.','Профиль','Длина','Вес','Марка стали',inf[oper]['oper'],'отв','скос','вырез','фаска','фрез','гибка']
  elif oper == 'weld':
    widthList = [width/9]
    table_list = ['Конструкция','Марка','Чертеж','Колич.','Ствол','Масса','Кол. деталей','Тариф сборка','Тариф сварка']
  elif oper == 'paint':
    widthList = [width/7]
    table_list = ['Конструкция','Марка','Колич.','Ствол','Масса','Кол. деталей','Тариф']
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

def Body2(width,height,inf,oper):
  if oper != 'weld' and oper != 'paint':
    widthList = [60,35,30,20,25,110,35,30,50,25,25,25,25,25,25,25]
    mas = inf[oper]['tabl']
    size = height/len(mas)
  elif oper == 'weld':
    widthList = [width/9]
    if len(str(inf['master'].part.profile).split(' ')) > 1:
      string = str(inf['master'].part.profile).split(' ')[0]+' '+str(inf['master'].part.profile).split(' ')[1][0:2]+' '+str(inf['master'].part.size)
    else:
      string = str(inf['master'].part.profile).split(' ')[0]+' '+str(inf['master'].part.size)
    mas = [[
      inf[oper]['tabl'].point.name,
      inf[oper]['tabl'].point.assembly.assembly,
      inf[oper]['tabl'].point.draw,
      1,
      string,
      float(inf[oper]['tabl'].point.assembly.weight),
      inf[oper]['tabl'].count,
      round(inf[oper]['norm_assembly']),
      round(inf[oper]['norm_weld']),
    ]]
    size = height

  elif oper == 'paint' and inf['weld']['tabl'] != None:
    widthList = [width/7]
    if len(str(inf['master'].part.profile).split(' ')) > 1:
      string = str(inf['master'].part.profile).split(' ')[0]+' '+str(inf['master'].part.profile).split(' ')[1][0:2]+' '+str(inf['master'].part.size)
    else:
      string = str(inf['master'].part.profile).split(' ')[0]+' '+str(inf['master'].part.size)
    mas = [[
      inf[oper]['tabl'].point.name,
      inf[oper]['tabl'].point.assembly.assembly,
      1,
      string,
      float(inf[oper]['tabl'].point.assembly.weight),
      inf[oper]['tabl'].count,
      '',
    ]]
    size = height

  elif oper == 'paint' and inf['weld']['tabl'] == None:
    widthList = [width/7]
    # if len(str(inf['master'].part.profile).split(' ')) > 1:
    #   string = str(inf['master'].part.profile).split(' ')[0]+' '+str(inf['master'].part.profile).split(' ')[1][0:2]+' '+str(inf['master'].part.size)
    # else:
    #   string = str(inf['master'].part.profile).split(' ')[0]+' '+str(inf['master'].part.size)
    mas = inf[oper]['tabl2']
    size = height/len(mas)

  table = Table(mas
  ,colWidths=widthList,
    rowHeights=size)
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

def Body3(width,height,inf,oper):
  if oper != 'weld' and oper != 'paint':
    widthList = [60,35,30,20,25,110,35,30,50,25,25,25,25,25,25,25]
    # table = Table([['','','','',inf[oper]['tabl_sum']['table_count'],'','',float(inf[oper]['tabl_sum']['table_weight']),'','','','','','','','']]
    table = Table([['','','','','','','',float(inf[oper]['tabl_sum']['table_weight']),'','','','','','','','']]
    ,colWidths=widthList,
      rowHeights=12)
    table.setStyle([
      # ('GRID',(4,0),(4,0),1,'black'),
      ('GRID',(7,0),(7,0),1,'black'),
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
  else:
    return ''



def Inf(details,case):
  inf_pdf = []
  for detail in details:
    inf1 = PointPart.select(PointPart,(fn.SUM(Part.count) * Part.weight).alias('weight'),fn.SUM(Part.count).alias('count')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work == 'saw_b').group_by(Part.number)
    inf2 = PointPart.select(PointPart,(fn.SUM(Part.count) * Part.weight).alias('weight'),fn.SUM(Part.count).alias('count')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work == 'saw_s').group_by(Part.number)
    inf3 = PointPart.select(PointPart,(fn.SUM(Part.count) * Part.weight).alias('weight'),fn.SUM(Part.count).alias('count')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work == 'cgm').group_by(Part.number)
    inf4 = PointPart.select(fn.SUM(Part.count).alias('count'),PointPart).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case)
    inf7 = PointPart.select().join(Point).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case).group_by(PointPart.point).count()
    inf5 = PointPart.select(Part.profile,Part.size,fn.MAX(Part.weight).alias('weight')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work != 'cgm').first()
    if inf4.scalar() > 1 and inf7 == 1:
      inf6 = PointPart.select(PointPart,fn.SUM(Part.count).alias('count')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case).first()
      try:
        norm = Drawing.select(Drawing.weight,Drawing.count,Point.name,fn.SUM(Part.count).alias('count_p')).join(Part).join_from(Drawing,Point).where(Drawing.id == inf6.part.assembly).first()
        norm_assembly = AssemblyNorm.select().where(AssemblyNorm.name == norm.point.name,
                                                    norm.weight >= AssemblyNorm.mass_of,
                                                    norm.weight < AssemblyNorm.mass_to,
                                                    inf6.count >= AssemblyNorm.count_of,
                                                    inf6.count < AssemblyNorm.count_to).first()
        norm_assembly = (norm_assembly.norm * (norm.weight/1000))
      except:
        norm_assembly = 0
      try:
        norm_w = Weld.select().where(Weld.assembly == inf6.part.assembly)
        norm_weld = 0
        for w in norm_w:
          weld = WeldNorm.select((WeldNorm.norm * w.length / 1000 / norm.count).alias('aaa')).where(WeldNorm.cathet == w.cathet).first()
          norm_weld += weld.aaa
      except:
        norm_weld = 0
    else:
      inf6 = None
      norm_assembly = None
    inf8 = PointPart.select(PointPart,fn.SUM(Part.count).alias('count')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case).first()
    gr = PointPart.select(Part.work,PointPart.point,
                          fn.SUM(Part.weight * Part.count).alias('weight'),
                          fn.SUM(Part.count).alias('count'),
                          fn.SUM(PointPart.saw).alias('saw'),
                          fn.SUM(PointPart.cgm).alias('cgm'),
                          fn.SUM(Case(None, [((PointPart.hole == 1) & (Part.size.cast('int') >= 14) & (PointPart.cgm == 1),1)], 0)).alias('hole_cgm'),
                          fn.SUM(Case(None, [((PointPart.hole == 1) & (PointPart.saw == 1),1)], 0)).alias('hole_saw'),
                          fn.SUM(PointPart.bevel).alias('bevel'),
                          fn.SUM(PointPart.notch).alias('notch'),
                          fn.SUM(PointPart.chamfer).alias('chamfer'),
                          fn.SUM(PointPart.milling).alias('milling'),
                          fn.SUM(PointPart.bend).alias('bend'),
                  ).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case).group_by(Part.work).objects()
    faza = gr[0].point.faza
    gr1 = {'saw_s':{'weight': None, 'count': None},'saw_b':{'weight': None, 'count': None},'cgm':{'weight': None, 'count': None}}
    gr2 = []
    gr3 = ['Пм','Пб','Сп','В','Ф','Сф','F','W','M']
    gr4 = ''
    for i in gr:
      gr1[i.work] = {'weight': i.weight, 'count': i.count}
      if i.saw > 0 and i.work == 'saw_s':
        gr2.append('Пм')
      if i.saw > 0 and i.work == 'saw_b':
        gr2.append('Пб')
      if i.cgm > 0:
        gr2.append('Ф')
      if i.hole_cgm > 0:
        gr2.append('Сф')
      if i.notch > 0:
        gr2.append('В')
      if i.hole_saw > 0:
        gr2.append('Сп')
      if i.chamfer > 0:
        gr2.append('F')
      if inf4.scalar() > 1 and inf7 == 1:
        gr2.append('W')
      gr2.append('M')
    for i in gr3:
      if i in gr2:
        gr4 += i+' '
    gr2 = gr4
      
    inf = {'saw_b':inf1,'saw_s':inf2,'cgm':inf3}
    tabl_saw_s = {'tabl':[],'tabl_sum':{'table_count':gr1['saw_s']['count'],'table_weight':gr1['saw_s']['weight']},'name':'ПИЛЫ М','color':colors.blue,'color_t':'white','oper':'пилы'}
    tabl_saw_b = {'tabl':[],'tabl_sum':{'table_count':gr1['saw_b']['count'],'table_weight':gr1['saw_b']['weight']},'name':'ПИЛЫ Б','color':colors.green,'color_t':'white','oper':'пилы'}
    tabl_cgm = {'tabl':[],'tabl_sum':{'table_count':gr1['cgm']['count'],'table_weight':gr1['cgm']['weight']},'name':'ФАСОНКА','color':colors.yellow,'color_t':'black','oper':'цгм'}
    tabl_weld = {'tabl':inf6,'norm_assembly': norm_assembly,'norm_weld': norm_weld,'name':'Сборка','color':colors.red,'color_t':'black','count':inf4.scalar()}
    tabl_paint ={'tabl':inf8,'tabl2':[],'name':'Малярка','color':colors.pink,'color_t':'black','count':inf4.scalar()}
    for y in inf:
      for i in inf[y]:
        tab = []
        tab2 = []
        tab.append(i.point.name)
        tab2.append(i.point.name)
        tab.append(i.point.assembly.assembly)
        tab2.append(i.point.assembly.assembly)
        tab.append(i.point.draw)
        tab.append(i.part.number)
        tab.append(i.count)
        tab2.append(i.count)
        if len(i.part.profile.split(' ')) > 1:
          tab.append((i.part.profile).split(' ')[0]+' '+(i.part.profile).split(' ')[1][0:2]+' '+i.part.size)
          tab2.append((i.part.profile).split(' ')[0]+' '+(i.part.profile).split(' ')[1][0:2]+' '+i.part.size)
        elif i.part.profile == 'Лист':
          tab.append((i.part.profile)+' '+i.part.size+'х'+i.part.width)
          tab2.append((i.part.profile)+' '+i.part.size+'х'+i.part.width)
        else:
          tab.append((i.part.profile)+' '+i.part.size)
          tab2.append((i.part.profile)+' '+i.part.size)
        tab.append(int(i.part.length))
        tab.append(float(i.weight))
        tab2.append(float(i.weight))
        tab.append(i.part.mark)
        if i.saw == 1:
          try:
            saw = SawNorm.select().where(SawNorm.profile == i.part.profile,SawNorm.size == i.part.size).first()
            tab.append(round(saw.norm_direct * i.count))
          except:
            print(i.part.profile,i.part.size,'111')
            tab.append('+')
        else:
          tab.append('+')

        tab2.append(1)

        if i.hole == 1:
          try:
            hole = Hole.select().where(Hole.part == i.part).first()
            if y == 'cgm' and int(i.part.size) >= 14:
              norm = HoleNorm.select().where(HoleNorm.diameter >= hole.diameter,
                                            HoleNorm.depth_of <= i.part.depth,
                                            HoleNorm.depth_to >= i.part.depth,
                                            HoleNorm.count >= hole.count,
                                            HoleNorm.metal == 'Лист').first()
              tab.append(round(norm.norm * hole.count * i.count))
            elif y != 'cgm':
              norm = HoleNorm.select().where(HoleNorm.diameter >= hole.diameter,
                                            HoleNorm.lenght_of <= int(i.part.length),
                                            HoleNorm.lenght_to >= int(i.part.length),
                                            HoleNorm.depth_of <= i.part.depth,
                                            HoleNorm.depth_to >= i.part.depth,
                                            HoleNorm.count >= hole.count,
                                            HoleNorm.metal == 'Сорт').first()
              tab.append(round(norm.norm * hole.count * i.count))
            else:
              tab.append('')
          except:
            print(i.part.profile,i.part.size,'222')
            tab.append('0')
        else:
          tab.append('')
        if i.bevel == 1:
          tab.append('+')
        else:
          tab.append('')
        if i.notch == 1:
          tab.append('+')
        else:
          tab.append('')
        if i.chamfer == 1:
          tab.append('+')
        else:
          tab.append('')
        if i.milling == 1:
          tab.append('+')
        else:
          tab.append('')
        if i.bend == 1:
          tab.append('+')
        else:
          tab.append('')
        if y == 'saw_s':
          tabl_saw_s['tabl'].append(tab)
        if y == 'saw_b':
          tabl_saw_b['tabl'].append(tab)
        if y == 'cgm':
          tabl_cgm['tabl'].append(tab)
        tab2.append('')
        tabl_paint['tabl2'].append(tab2)
    inf_pdf.append({'case':case,'detail':detail,'work':gr2,'master':inf5,'faza':faza,'saw_s':tabl_saw_s,'saw_b':tabl_saw_b,'cgm':tabl_cgm,'weld':tabl_weld,'paint':tabl_paint,'name':inf4[0].point.name,'mark':inf4[0].point.assembly.assembly,'color':inf4[0].point.assembly.cas.color})
  Pdf(inf_pdf)
  return



