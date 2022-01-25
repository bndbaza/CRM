from models import Drawing, Order, Point, Part, PointPart
from db import connection
from peewee import fn, JOIN
from openpyxl import load_workbook

def Faza_update(order):
  post = []
  points = Point.select().where(Order.cas == order).join(Drawing).join(Order).order_by(Point.point_z,Point.point_y,Point.point_x)
  line=1
  faza=1
  weight=0
  for row in points:
    row.line = line
    line += 1
    weight += row.assembly.weight
    if weight > 15000:
      weight = row.assembly.weight
      faza += 1
    row.faza = faza
    post.append(row)
  Point.bulk_update(post, fields=[Point.line,Point.faza])

def Faza_update_test(order):
  wb = load_workbook('faza.xlsx',data_only=True)
  sheet = wb.get_sheet_by_name('2313.3')
  for i in range(1,145):
    try:
      drawing = Drawing.select().where(Drawing.assembly == (sheet.cell(row=i,column=1).value)).first()
      point = Point.update({Point.faza: sheet.cell(row=i,column=3).value}).where(Point.assembly == drawing)
      return point[0]
    except:
      pass


def PartPoint(faza,cas):
  parts = Part.filter(assembly__cas__cas = cas)
  points = Point.filter(faza = faza,assembly__cas__cas = cas)
  maxpp = PointPart.select(fn.MAX(PointPart.detail)).scalar()
  all = []
  if maxpp == None:
    maxpp = 1
  else:
    maxpp += 1
  for point in points:
    for part in parts:
      if point.assembly == part.assembly:
        oper = {'hole': 0, 'chamfer': 0, 'cgm': 0, 'saw': 0, 'milling': 0}
        if part.chamfers.count() > 0:
          oper['chamfer'] = 1
        if part.holes.count() > 0:
          oper['hole'] = 1
        if part.profile == 'Лист':
          oper['cgm'] = 1
        else:
          oper['saw'] = 1
        if part.manipulation.find('фрез') >= 0:
          oper['milling'] = 1
        d = (point,part,maxpp,oper['hole'],oper['chamfer'],oper['cgm'],oper['saw'],oper['milling'])
        all.append(d)
    maxpp += 1
  with connection.atomic():
    PointPart.insert_many(all, fields=[PointPart.point,PointPart.part,PointPart.detail,PointPart.hole,PointPart.chamfer,PointPart.cgm,PointPart.saw,PointPart.milling]).execute()
  Test()

def Test2():
  z = PointPart.select(PointPart).join(Part).join(Drawing)
  y = 1
  case = z[0].point.assembly
  all = []
  for i in z:
    if i.point.assembly != case:
      print(i.point.assembly,case)
      y += 1
    i.detail = y
    case = i.point.assembly
    all.append(i)
  PointPart.bulk_update(all, fields=[PointPart.detail])
  
def Test():
  zi = PointPart.select(PointPart,fn.COUNT(PointPart.detail).alias('aaa')).group_by(PointPart.detail).having(fn.COUNT(PointPart.detail) != 1)
  yi = PointPart.select(PointPart,fn.COUNT(PointPart.detail).alias('aaa')).group_by(PointPart.detail).having(fn.COUNT(PointPart.detail) == 1)
  xi = PointPart.select()
  index = 1
  all = []
  for i in zi:
    i.detail = index
    index += 1
  dec = {}
  for i in yi:
    if i.part.profile+i.part.size in dec.keys():
      i.detail = dec[i.part.profile+i.part.size]
    else:
      dec[i.part.profile+i.part.size] = index
      i.detail = index
      index += 1
  for i in xi:
    for y in yi:
      if i.point == y.point:
        i.detail = y.detail
        all.append(i)
  for i in xi:
    for y in zi:
      if i.point == y.point:
        i.detail = y.detail
        all.append(i)
  PointPart.bulk_update(all, fields=[PointPart.detail])




    

  # y = PointPart.select()
  # index = 1
  # mono = []
  # all =[]
  # for i in y:
  #   for v in z:
  #     if v.aaa == 1 and i.detail == v.detail:
  #       pass
  #       # i.detail = 0
  #       # all.append(i)
  #     if v.aaa != 1 and i.detail == v.detail:
  #       i.detail = index
  #       index += 1
  #   all.append(i)
  # PointPart.bulk_update(all, fields=[PointPart.detail])

