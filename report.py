from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

def Pdf(inf):
  inf = Inf(inf)
  pdf = canvas.Canvas('My.pdf', pagesize=A4,bottomup=1)
  pdf.setTitle('test')
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02,]
  heightList = [height*0.015,height*0.97,height*0.015,]
  mainTable = Table([
    ['','',''],
    ['',PrintTab(widthList[1],heightList[1],inf),''],
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
  pdf.showPage()
  pdf.save()


def PrintTab(width,height,inf):
  heightList = [height*0.1,height*0.25,height*0.15,height*0.1,height*0.25,height*0.15]
  table = Table([
    [Header1(width,heightList[0],inf)],
    [Body(width,heightList[1],inf)],
    [Footer(width,heightList[2],inf)],
    [Header1(width,heightList[0],inf)],
    [Body(width,heightList[1],inf)],
    [Footer(width,heightList[2],inf)]
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table


def Header1(width,height,inf):
  widthList = [90,width-90]
  img = Image('aut.gif',widthList[0],height)
  table = Table([
    [img,Header2(widthList[1],height,inf)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(0,0),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Header2(width,height,inf):
  heightList = [height*0.2,height*0.3,height*0.5]
  table = Table([
    [''],
    [Header3(width,heightList[1],inf)],
    ['']
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table


def Header3(width,height,inf):
  widthList = [width*0.1,width*0.2,width*0.2,width*0.2,width*0.1,width*0.2]
  table = Table([
    ['Пр','ПИЛЫ','№'+str(inf[2]),inf[0],inf[1],'P C W M'],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
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

def Footer(width,height,inf):
  widthList = [width*0.4,width*0.2,width*0.4]
  image_run = 'run.gif'
  image_aut = 'aut.gif'
  table = Table([
    [Footer1(widthList[0],height,'Бегунок',image_run,inf),'',Footer1(widthList[0],height,'Авторизация',image_aut,inf)],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(0,0),1,'black'),
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer1(width,height,str,image,inf):
  heightList = [height*0.1,height*0.5,height*0.1,height*0.3]
  table = Table([
    [Footer2(width,heightList[0],str,inf)],
    [Footer3(width,heightList[1],inf)],
    [Footer4(width,heightList[2],inf)],
    [Footer5(width,heightList[3],image,inf)]
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(-1,-1),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
  ])
  return table

def Footer2(width,height,str,inf):
  widthList = [width*0.1,width*0.8,width*0.1]
  table = Table([
    [inf[1],str,inf[3][0][0][0]],
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Footer3(width,height,inf):
  table = Table([
    [inf[2]],
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

def Footer4(width,height,inf):
  widthList = [width*0.5,width*0.5]
  table = Table([
    [inf[3][0][1],'П С W M'],
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

def Footer5(width,height,image,inf):
  widthList = [width*0.25,width*0.5,width*0.1,width*0.15]
  img = Image(image,widthList[1],height,kind='proportional')
  table = Table([
    [Footer6(widthList[0],height,inf),img,'Пр',inf[0]],
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


def Footer6(width,height,inf):
  heightList = [height/3,height/3,height/3]
  table = Table([
    [inf[3][0][4]],
    [inf[4]],
    [inf[5]],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(0,0),(0,1),'RIGHT'),
    ('ALIGN',(-1,-1),(-1,-1),'CENTER'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Body(width,height,inf):
  heightList = [20,len(inf[3])*15,height-20-(len(inf[3]*15))]
  table = Table([
    [Body1(width,heightList[0],inf)],
    [Body2(width,heightList[1],inf)],
    ['']
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

def Body1(width,height,inf):
  widthList = [60,35,25,30,60,35,30,50,25,25,25,25,25,25,25,]
  table = Table([
    ['Конструкция','Марка','№','Колич.','Профиль','Длинна','Вес','Марка стали',('пилы'),('отв'),
    ('скос'),('вырез'),('фаска'),('фрез'),('гибка')],
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

def Body2(width,height,inf):
  widthList = [60,35,25,30,60,35,30,50,25,25,25,25,25,25,25,]
  mas = inf[3]
  table = Table(mas
  ,colWidths=widthList,
    rowHeights=height/len(mas))
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    # ('LEFTPADDING',(0,0),(-1,-1),0),
    # ('RIGHTPADDING',(0,0),(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    # ('TOPPADDING',(0,0),(-1,-1),0),
    # ('PADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),8),
    # ('ALIGN',(0,0),(0,1),'RIGHT'),
    # ('ALIGN',(0,0),(-1,-1),'CENTER'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Inf(inf):
  count = inf[1]
  mass = inf[2]
  inf = inf[0]
  case = inf[0].part.assembly.cas.cas
  faza = inf[0].point.faza
  detail = inf[0].detail
  tabl = []
  for i in inf:
    tab = []
    tab.append('Балка')
    tab.append(i.point.assembly.assembly)
    tab.append(i.part.number)
    tab.append(i.part.count)
    tab.append(i.part.profile)
    tab.append(i.part.length)
    tab.append(i.part.weight)
    tab.append(i.part.mark)
    tab.append(i.saw)
    tab.append(i.hole)
    tab.append(i.bevel)
    tab.append(i.notch)
    tab.append(i.chamfer)
    tab.append(i.milling)
    tab.append(i.bend)
    tabl.append(tab)
  return [case,faza,detail,tabl,count,mass]



