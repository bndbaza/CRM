from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from models import *
from peewee import fn, JOIN

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

def Pdf(inf):
  lis = []
  pdf = canvas.Canvas('My.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')
  if inf['saw_s']['tabl_sum']['table_count'] != None:
    lis.append('saw_s')
  if inf['saw_b']['tabl_sum']['table_count'] != None:
    lis.append('saw_b')
  if inf['cgm']['tabl_sum']['table_count'] != None:
    lis.append('cgm')
  for i in range(len(lis)//2 + len(lis)%2):
    lis2 = []
    lis2.append(lis.pop(0))
    try:
      lis2.append(lis.pop(0))
    except:
      pass
    Pdf1(inf,pdf,lis2)
    pdf.showPage()
  pdf.save()



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
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
  ])
  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)


def PrintTab(width,height,inf,lis):
  heightList = [height*0.07,height*0.28,height*0.15,height*0.07,height*0.28,height*0.15]
  lis2 = [
    [Header1(width,heightList[0],inf,lis[0])],
    [Body(width,heightList[1],inf,lis[0])],
    [Footer(width,heightList[2],inf,lis[0])],
  ]
  if len(lis) == 2:
    lis2.append([Header1(width,heightList[3],inf,lis[1])])
    lis2.append([Body(width,heightList[4],inf,lis[1])])
    lis2.append([Footer(width,heightList[5],inf,lis[1])])
  else:
    for i in range(3):
      lis2.append([''])
  table = Table(lis2,colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table


def Header1(width,height,inf,oper):
  widthList = [80,width-80]
  img = Image('aut.gif',widthList[0],height,kind='proportional')
  table = Table([
    [img,Header2(widthList[1],height,inf,oper)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(0,0),1,'red'),
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
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table


def Header3(width,height,inf,oper):
  widthList = [width*0.1,width*0.2,width*0.2,width*0.2,width*0.1,width*0.2]
  table = Table([
    [inf[oper]['tabl'][0][0][0],inf[oper]['name'],'№'+str(inf['detail']),inf['case'],inf['faza'],inf['work'][oper]],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('BACKGROUND',(1,0),(1,0),inf[oper]['color']),
    ('BACKGROUND',(3,0),(3,0),colors.green),
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
  image_run = 'run.gif'
  image_aut = 'aut.gif'
  table = Table([
    [Footer1(widthList[0],height,'Бегунок',image_run,inf,oper),'',Footer1(widthList[0],height,'Авторизация',image_aut,inf,oper)],
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
  widthList = [width*0.1,width*0.8,width*0.1]
  table = Table([
    [inf['faza'],str,inf[oper]['name'][0]],
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
    # ('GRID',(0,0),(-1,-1),1,'red'),
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
    [inf[oper]['tabl'][0][1],inf['work'][oper]],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(-1,-1),(-1,-1),'RIGHT'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('FONTSIZE',(0,0),(-1,-1),60),
  ])
  return table

def Footer5(width,height,image,inf,oper):
  widthList = [width*0.25,width*0.4,width*0.1,width*0.25]
  img = Image(image,widthList[1],height,kind='proportional')
  table = Table([
    [Footer6(widthList[0],height,inf,oper),img,inf[oper]['tabl'][0][0][0],inf['case']],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(0,0),1,'black'),
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,0),0),
    ('BOTTOMPADDING',(0,0),(-1,0),0),
    ('TOPPADDING',(0,0),(-1,0),0),
    ('RIGHTPADDING',(0,0),(-1,0),0),
    # ('BOTTOMPADDING',(-2,0),(-1,0),13),
    ('BACKGROUND',(-1,0),(-1,0),colors.green),
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

  # if inf[oper]['tabl'][0][4].startswith('Лист'):
  #   i = inf[oper]['tabl'][0][4].split(' ')[1].split('x')[1]
  # else:
  #   i = inf[oper]['tabl'][0][4].split(' ')[1]

  table = Table([
    [i],
    [inf[oper]['tabl_sum']['table_count']],
    [float(inf[oper]['tabl_sum']['table_weight'])],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('FONTSIZE',(0,0),(0,0),8),
    # ('ALIGN',(0,0),(0,1),'RIGHT'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body(width,height,inf,oper):
  heightList = [20,len(inf[oper]['tabl'])*12,12,height-20-12-(len(inf[oper]['tabl']*12))]
  table = Table([
    [Body1(heightList[0],inf,oper)],
    [Body2(heightList[1],inf,oper)],
    [Body3(width,heightList[2],inf,oper)],
    [''],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('ROTATE',(0,0),(0,0),90),
    # ('FONTNAME',(0,0),(-1,-1),'rus'),
    # ('ALIGN',(0,0),(0,1),'RIGHT'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body1(height,inf,oper):
  widthList = [60,35,25,30,60,35,30,50,25,25,25,25,25,25,25,]
  table = Table([
    ['Конструкция','Марка','№','Колич.','Профиль','Длинна','Вес','Марка стали',inf[oper]['oper'],'отв',
    'скос','вырез','фаска','фрез','гибка'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),8),
    # ('ALIGN',(0,0),(0,1),'RIGHT'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body2(height,inf,oper):
  widthList = [60,35,25,30,60,35,30,50,25,25,25,25,25,25,25,]
  mas = inf[oper]['tabl']
  table = Table(mas
  ,colWidths=widthList,
    rowHeights=height/len(mas))
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    # ('PADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),8),
    # ('ALIGN',(0,0),(0,1),'RIGHT'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body3(width,height,inf,oper):
  widthList = [60,35,25,30,60,35,30,50,25,25,25,25,25,25,25,]
  table = Table([['','','',inf[oper]['tabl_sum']['table_count'],'','',float(inf[oper]['tabl_sum']['table_weight']),'','','','','','','','']]
  ,colWidths=widthList,
    rowHeights=12)
  table.setStyle([
    ('GRID',(3,0),(3,0),1,'black'),
    ('GRID',(6,0),(6,0),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    # ('PADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),8),
    # ('ALIGN',(0,0),(0,1),'RIGHT'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table







def Inf(detail,case):
  inf1 = PointPart.select().join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work == 'saw_b')
  inf2 = PointPart.select().join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work == 'saw_s')
  inf3 = PointPart.select().join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work == 'cgm')
  inf4 = PointPart.select(fn.SUM(Part.count).alias('count')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case).scalar()
  inf5 = PointPart.select(Part.profile,Part.size,fn.MAX(Part.weight).alias('weight')).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case,Part.work != 'cgm').first()
  gr = PointPart.select(Part.work,PointPart.point,
                        fn.SUM(Part.weight).alias('weight'),
                        fn.SUM(Part.count).alias('count'),
                        fn.SUM(PointPart.saw).alias('saw'),
                        fn.SUM(PointPart.cgm).alias('cgm'),
                        fn.SUM(PointPart.hole).alias('hole'),
                        fn.SUM(PointPart.bevel).alias('bevel'),
                        fn.SUM(PointPart.notch).alias('notch'),
                        fn.SUM(PointPart.chamfer).alias('chamfer'),
                        fn.SUM(PointPart.milling).alias('milling'),
                        fn.SUM(PointPart.bend).alias('bend'),
                ).join(Part).join(Drawing).join(Order).where(PointPart.detail == detail,Order.cas == case).group_by(Part.work).objects()
  faza = gr[0].point.faza
  gr1 = {'saw_s':{'weight': None, 'count': None},'saw_b':{'weight': None, 'count': None},'cgm':{'weight': None, 'count': None}}
  gr2 = {'saw_s':'','saw_b':'','cgm':''}
  for i in gr:
    gr1[i.work] = {'weight': i.weight, 'count': i.count}
    if i.saw > 0:
      gr2[i.work] = gr2[i.work] + 'П'
    if i.cgm > 0:
      gr2[i.work] = gr2[i.work] + 'Ф'
    if i.hole > 0:
      gr2[i.work] = gr2[i.work] + ' С'
    if i.chamfer > 0:
      gr2[i.work] = gr2[i.work] + ' F'
    if inf4 > 1:
      gr2[i.work] = gr2[i.work] + ' W'
    gr2[i.work] = gr2[i.work] + ' М'
    
  inf = {'saw_b':inf1,'saw_s':inf2,'cgm':inf3}
  tabl_saw_s = {'tabl':[],'tabl_sum':{'table_count':gr1['saw_s']['count'],'table_weight':gr1['saw_s']['weight']},'name':'ПИЛЫ М','color':colors.blue,'color_t':'white','oper':'пилы'}
  tabl_saw_b = {'tabl':[],'tabl_sum':{'table_count':gr1['saw_b']['count'],'table_weight':gr1['saw_b']['weight']},'name':'ПИЛЫ Б','color':colors.green,'color_t':'white','oper':'пилы'}
  tabl_cgm = {'tabl':[],'tabl_sum':{'table_count':gr1['cgm']['count'],'table_weight':gr1['cgm']['weight']},'name':'ФАСОНКА','color':colors.yellow,'color_t':'black','oper':'цгм'}
  for y in inf:
    for i in inf[y]:
      tab = []
      tab.append(i.point.name)
      tab.append(i.point.assembly.assembly)
      tab.append(i.part.number)
      tab.append(i.part.count)
      tab.append(i.part.profile+' '+i.part.size)
      tab.append(int(i.part.length))
      tab.append(float(i.part.weight))
      tab.append(i.part.mark)
      if i.saw == 1:
        tab.append('+')
      else:
        tab.append('+')
      if i.hole == 1:
        tab.append('+')
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
  Pdf({'case':case,'detail':detail,'work':gr2,'master':inf5,'faza':faza,'saw_s':tabl_saw_s,'saw_b':tabl_saw_b,'cgm':tabl_cgm})
  return



