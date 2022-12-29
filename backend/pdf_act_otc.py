from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image, Paragraph
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib import colors
from datetime import date, datetime
from peewee import fn, JOIN, Case

from models import Detail, Faza, Otc, PointPart

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

oper = ''

def ActEveryDay(today,work):
  global oper
  oper = work
  pdf = canvas.Canvas(f'media/acts/atc{today} {oper}.pdf', pagesize=landscape(A4))
  cases = Otc.select().join(Faza).where(Otc.oper == oper,Otc.end >= today,Otc.end <= datetime(today.year,today.month,today.day,23,59,59)).group_by(Faza.case)
  for case in cases:
    tab = Otc.select().join(Faza).where(Faza.case == case.detail.case,Otc.oper == oper,Otc.end >= today,Otc.end <= datetime(today.year,today.month,today.day,23,59,59))
    if len(tab) == 0:
      return ''
    list = []
    tabs = []
    x = 1
    for i in tab:
      if oper == 'weld':
        pp = PointPart.select().where(PointPart.detail == i.detail.detail).first()
        weld = Detail.select().where(Detail.detail == i.detail.detail,Detail.oper == 'weld').first()
        if weld.worker_2 == None:
          weld = f'{weld.worker_1.user.surname}'
        else:
          weld = f'{weld.worker_1.user.surname}, {weld.worker_2.user.surname}'
        assembly = Detail.select().where(Detail.detail == i.detail.detail,Detail.oper == 'assembly').first()
        if assembly.worker_2 == None:
          assembly = f'{assembly.worker_1.user.surname}'
        else:
          assembly = f'{assembly.worker_1.user.surname}, {assembly.worker_2.user.surname}'
      elif oper == 'paint':
        pp = PointPart.select().where(PointPart.detail == i.detail.detail).first()
        weld = Detail.select().where(Detail.detail == i.detail.detail,Detail.oper == 'paint').first()
        try:
          if weld.worker_2 == None:
            weld = f'{weld.worker_1.user.surname}'
          else:
            weld = f'{weld.worker_1.user.surname}, {weld.worker_2.user.surname}'
        except:
          weld = 'Без покраски'
        assembly = ''

      text = ''
      if i.usc:
        text = 'УЗК'
      tabs.append([pp.point.draw,pp.point.assembly.assembly,i.detail.detail,1,float(pp.point.assembly.weight),weld,assembly,f'{i.worker.user.surname} {i.worker.user.name[0]}.{i.worker.user.patronymic[0]}',text])
      x += 1
      if x == 31 and len(tab) != 30:
        list.append(tabs)
        tabs = []
        x = 1
    list.append(tabs)
    pdf.setTitle('')
    for lis in list:
      if len(lis) > 0:
        cas = case.detail.case.cas
        Pdf(cas,pdf,lis,today)
        pdf.showPage()
  pdf.save()
  return f'{today}z{oper}'

def Pdf(case,pdf,lis,today):
  width, height = landscape(A4)
  widthList = [width*0.02,width*0.96,width*0.02]
  heightList = [height*0.015,height*0.96,height*0.025]
  mainTable = Table([
    ['','',''],
    ['',Hub(case,lis,today,widthList[1],heightList[1]),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
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


def Hub(case,tabs,today,width,height):
  heightList = [height * 0.1,height * 0.05,len(tabs) * 15,(height * 0.85) - (len(tabs) * 15)]
  table = Table([
    [Header(case,today,width,heightList[0])],
    [Body1(width,heightList[1])],
    [Body2(tabs,width,heightList[2])],
    ['Представитель ОТК______________'],
  ],colWidths=width,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    # ('GRID',(0,1),(0,1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('VALIGN',(-1,-1),(-1,-1),'TOP'),
    ('TOPPADDING',(-1,-1),(-1,-1),20),
  ])
  return table

def Header(case,today,width,height):
  heightList = height / 3
  widthList = width / 3
  zona = 'Сборочно-сварочный участок'
  if oper == 'paint':
    zona = 'Малярный участок'
  table = Table([
    [zona,'Акт приемки продукции',''],
    ['',f'Заказ № {case}',''],
    [today.strftime("%d.%m.%Y"),'','']
  ],colWidths=widthList,
    rowHeights=heightList)
  table.setStyle([
    # ('GRID',(0,0),(-1,-1),1,'red'),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(1,2),'CENTER'),
    ('FONTSIZE',(0,0),(0,2),9),
    # ('GRID',(0,1),(0,1),1,'black'),
    # ('LEFTPADDING',(0,0),11(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    # ('ALIGN',(0,-2),(0,-2),'RIGHT'),
    # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('TOPPADDING',(0,0),(0,0),0),
    # ('VALIGN',(0,0),(0,0),'TOP'),
  ])
  return table

def Body1(width,height):
  widthList = [90,80,90,60,60,140,140,80,width - 740]
  head = ['№ Чертежа','Марка элемента','Заводской номер','Количество','Масса','Сварщик','Сборщик','Принята ОТК','Примечание']
  if oper == 'paint':
    head = ['№ Чертежа','Марка элемента','Заводской номер','Количество','Масса','Маляр','','Принята ОТК','Примечание']
    widthList = [90,80,90,60,60,140,0,80,width - 600]

  table = Table([
    head,
  ],colWidths=widthList,
    rowHeights=height)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(1,2),'CENTER'),
    # ('FONTSIZE',(0,0),(0,2),7),
    # ('GRID',(0,1),(0,1),1,'black'),
    # ('LEFTPADDING',(0,0),11(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('TOPPADDING',(0,0),(0,0),0),
    # ('VALIGN',(0,0),(0,0),'TOP'),
  ])
  return table

def Body2(tabs,width,height):
  widthList = [90,80,90,60,60,140,140,80,width - 740]
  if oper == 'paint':
    widthList = [90,80,90,60,60,140,0,80,width - 600]
  # tabs = []
  # heightList = height / len(tabs)
  table = Table(tabs,colWidths=widthList,
    rowHeights=height / len(tabs))
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('ALIGN',(1,0),(1,2),'CENTER'),
    # ('FONTSIZE',(0,0),(0,2),7),
    # ('GRID',(0,1),(0,1),1,'black'),
    # ('LEFTPADDING',(0,0),11(-1,-1),0),
    # ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    # ('TOPPADDING',(0,0),(0,0),0),
    # ('VALIGN',(0,0),(0,0),'TOP'),
  ])
  return table
