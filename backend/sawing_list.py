from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from qr import QRTask
from peewee import fn, Case, Cast

from models import Drawing, Order, Part, Point, Task, TaskPart

pdfmetrics.registerFont(TTFont('rus','arial.ttf'))

stroka = 12

proc = {
  'weld':('Сварка','black','white'),
  'assembly':('Сборка','red','black'),
  'saw_b':('Пилы Б','blue','white'),
  'saw_s':('Пилы М','purple','white'),
  'hole':('Сверление','green','white'),
  'cgm':('Фасонка','yellow','black'),
  'bend':('Гибка','grey','black'),
  'milling':('Фрезеровка','brown','white'),
  'turning':('Токарка','white','black'),
  'bevel':('Скос','orange','black'),
  'notch':('Вырез','white','black'),
  'point':('Покраска','pink','black'),
  'chamfer':('Фаска','violet','black'),
  'joint':('Стык','black','white'),
  'no_metal':('Не металл','black','white')
}


def Sawing(faza,case):
  pdf = canvas.Canvas(f'reports/Задания {case} {faza}.pdf', pagesize=A4)
  pdf.setTitle('')
  tabl = Task.select().join(Order).where(Task.faza == faza,Order.cas == case)
  tabl1 = TaskPart.select(TaskPart,fn.COUNT(fn.DISTINCT(Part.number)).alias('count_tab')).join(Part).join_from(TaskPart,Task).where(TaskPart.task.in_(tabl)).group_by(Task.task)
  tabl3 = []
  for i in tabl1:
    tabl3.append(i)
  while len(tabl3) != 0:
    global stroka
    stroka = 12
    tabl2,tabl3 = Calc(tabl3)
    Border(pdf,tabl2)
    tabl2.clear()
    pdf.showPage()
  pdf.save()
  return f'reports/Задания {case} {faza}.pdf'

def Calc(tabl3):
  global stroka
  const = 816
  tab = []
  tab.extend(tabl3)
  tabl2 = []
  for i in tab:
    if i.count_tab > 60:
      stroka = (816 - 90) / i.count_tab
    # else:
    #   stroka = 12
    if (const - (90+stroka*i.count_tab)) >= 0:
      const = const - (90+stroka*i.count_tab)
      tabl2.append(i)
      tabl3.remove(i)
  return (tabl2,tabl3)

def Border(pdf,tabl):
  width, height = A4
  widthList = [width*0.02,width*0.96,width*0.02]
  heightList = [height*0.015,height*0.97,height*0.015,]
  mainTable = Table([
    ['','',''],
    ['',Page(tabl,widthList[1],heightList[1]),''],
    ['','',''],
  ],colWidths=widthList,
    rowHeights=heightList)
  mainTable.setStyle([
    # ('GRID',(1,1),(1,1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),20),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  mainTable.wrapOn(pdf,0,0)
  mainTable.drawOn(pdf,0,0)

def Page(tabl,width,height):
  heighList=[]
  tabList = []
  for i in tabl:
    heighList.append(90+stroka*i.count_tab)
    height -= 90+stroka*i.count_tab
    tabList.append([Page1(i.task,width,90+stroka*i.count_tab)])
  heighList.append(height)
  tabList.append([''])
  table = Table(tabList,colWidths=width,rowHeights=heighList)
  table.setStyle([
    ('GRID',(0,0),(-1,-1),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),14),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table

def Page1(tabl,width,height):
  heighList=[60,10,height-70]
  table = Table([
    [Header1(tabl,width,heighList[0])],
    [''],
    [Body(tabl,width,heighList[2])]
  ],colWidths=width,rowHeights=heighList)
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
  ])
  return table

def Header1(tabl,width,height):
  widthList=[60,(width-60)/4]
  img = Image(QRTask(tabl),widthList[0],height,kind='proportional')
  white = ('','white','black')
  table = Table([
    [img,Header2(proc[tabl.oper][0],proc[tabl.oper],widthList[1],height),Header2('Задание '+str(tabl.task),white,widthList[1],height),Header2('Заказ '+str(tabl.order.cas),('',tabl.order.color,'black'),widthList[1],height),Header2('Фаза '+str(tabl.faza),white,widthList[1],height)],
  ],colWidths=widthList,rowHeights=height)
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
  ])
  return table

def Header2(str,col,width,height):
  table = Table([
    [''],
    [str],
    [''],
  ],colWidths=width,rowHeights=height/3)
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
    ('BACKGROUND',(0,1),(0,1),col[1]),
    ('TEXTCOLOR',(0,1),(0,1),col[2])
  ])
  return table

def Body(tabl,width,height):
  tab = []
  heighList = []
  if tabl.oper == 'saw_b' or tabl.oper == 'saw_s':
    tab.append(['Чертеж','№ детали','Количество','Профиль','Размер','Длина','Вес','Марка стали','Обработка'])
  else:
    tab.append(['Чертеж','№ детали','Количество','Профиль','Размер','Длина','Вес','Марка стали'])
  heighList.append(stroka)
  height -= stroka
  for i in TaskPart.select(TaskPart,Drawing,Part,fn.SUM(TaskPart.count).alias('count_task')).join(Part).join(Drawing).where(TaskPart.task == tabl).group_by(Part.number).order_by(Part.number):
    x = ''
    if i.part.width != '':x='x'
    if i.part.assembly.points[0].draw == -1:
      draw = i.part.assembly.assembly
    else:
      draw = i.part.assembly.points[0].draw
    if tabl.oper == 'saw_b' or tabl.oper == 'saw_s':
      tab.append([
        draw,
        i.part.number,i.count_task,
        i.part.profile,
        i.part.size+x+i.part.width,
        int(i.part.length),
        float(i.part.weight),
        i.part.mark,
        i.part.manipulation
      ])
    else:
      tab.append([
        draw,
        i.part.number,i.count_task,
        i.part.profile,
        i.part.size+x+i.part.width,
        int(i.part.length),
        float(i.part.weight),
        i.part.mark
      ])
    heighList.append(stroka)
    height -= stroka
  heighList.append(height)
  tab.append([''])
  table = Table(tab,colWidths=width/(len(tab[0])),rowHeights=heighList)
  table.setStyle([
    ('GRID',(0,0),(-1,-2),1,'black'),
    ('LEFTPADDING',(0,0),(-1,-1),0),
    ('RIGHTPADDING',(0,0),(-1,-1),0),
    ('BOTTOMPADDING',(0,0),(-1,-1),0),
    ('TOPPADDING',(0,0),(-1,-1),0),
    ('FONTNAME',(0,0),(-1,-1),'rus'),
    ('FONTSIZE',(0,0),(-1,-1),9),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
  ])
  return table
