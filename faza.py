from models import Drawing, Order, Point, Part, PointPart, Basic_detail, Assembly_detail,Paint_detail
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
      drawing = Drawing.select().join(Order).where(Order.cas == order,Drawing.assembly == (sheet.cell(row=i,column=1).value)).first()
      point = Point.update({Point.faza: sheet.cell(row=i,column=3).value}).where(Point.assembly == drawing)
      return point[0]
    except:
      pass

def Faza_update_garage(order):
  drawing  = Drawing.select().join(Order).where(Order.cas == order)
  Point.update({Point.faza: 1}).where(Point.assembly << drawing,Point.point_x.cast('int') <= 3).execute()
  # Point.update({Point.faza: 3}).where(Point.assembly == 510,Point.point_x.cast('int') <= 3).execute()
  # Point.update({Point.faza: 2}).where(Point.assembly == 528).execute()
  # Point.update({Point.faza: 2}).where(Point.assembly == 529).execute()
  # Point.update({Point.faza: 2}).where(Point.assembly == 530).execute()
  Point.update({Point.faza: 2}).where(Point.assembly << drawing,Point.point_x.cast('int') > 3,Point.point_x.cast('int') <= 10).execute()
  Point.update({Point.faza: 2}).where(Point.assembly << drawing,Point.point_x.cast('int') > 10).execute()
  return



def PartPoint(faza,cas):
  parts = Part.filter(assembly__cas__cas = cas)
  points = Point.filter(faza = faza,assembly__cas__cas = cas)
  maxpp = PointPart.select(fn.MAX(PointPart.detail)).scalar()
  all = []
  if maxpp == None:
    maxpp = 1
  else:
    maxpp += 1
  max2 = maxpp
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
  Test(max2,faza,cas)

# def Test2():
#   z = PointPart.select(PointPart).join(Part).join(Drawing)
#   y = 1
#   case = z[0].point.assembly
#   all = []
#   for i in z:
#     if i.point.assembly != case:
#       print(i.point.assembly,case)
#       y += 1
#     i.detail = y
#     case = i.point.assembly
#     all.append(i)
#   PointPart.bulk_update(all, fields=[PointPart.detail])
  
def Test(max2,faza,case):
  # zi = PointPart.select(PointPart,fn.COUNT(PointPart.detail).alias('aaa')).group_by(PointPart.detail).having(fn.COUNT(PointPart.detail) != 1)
  # yi = PointPart.select(PointPart,fn.COUNT(PointPart.detail).alias('aaa')).group_by(PointPart.detail).having(fn.COUNT(PointPart.detail) == 1)
  # xi = PointPart.select()
  zi = PointPart.select(PointPart,fn.COUNT(PointPart.detail).alias('aaa')).join(Point).join(Drawing).join(Order).where(Point.faza == faza,Order.cas == case).group_by(PointPart.detail).having(fn.COUNT(PointPart.detail) != 1)
  yi = PointPart.select(PointPart,fn.COUNT(PointPart.detail).alias('aaa')).join(Point).join(Drawing).join(Order).where(Point.faza == faza,Order.cas == case).group_by(PointPart.detail).having(fn.COUNT(PointPart.detail) == 1)
  xi = PointPart.select().join(Point).join(Drawing).join(Order).where(Point.faza == faza,Order.cas == case)
  # index = PointPart.select(fn.MAX(PointPart.detail)).scalar()
  # print(index)
  index = max2
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
        i.weld = 0
        all.append(i)
  for i in xi:
    for y in zi:
      if i.point == y.point:
        i.detail = y.detail
        all.append(i)
  PointPart.bulk_update(all, fields=[PointPart.detail,PointPart.weld])

def Detail_create(faza,case):
  pointpart_work = PointPart.select(PointPart,
                                    fn.SUM(PointPart.hole),
                                    fn.SUM(PointPart.bevel),
                                    fn.SUM(PointPart.notch),
                                    fn.SUM(PointPart.chamfer),
                                    fn.SUM(PointPart.milling),
                                    fn.SUM(PointPart.bend)).join(Part).join(Drawing).join(Order).join_from(PointPart,Point).where(Order.cas == case,Point.faza == faza).group_by(PointPart.detail,Part.work)
  d = []
  for i in pointpart_work:
    d.append((i.detail,i.part.work,i.hole,i.bevel,i.notch,i.chamfer,i.milling,i.bend))
  Basic_detail.insert_many(d, fields=[Basic_detail.detail,Basic_detail.basic,Basic_detail.hole,Basic_detail.bevel,Basic_detail.notch,Basic_detail.chamfer,Basic_detail.milling,Basic_detail.bend]).execute()
  d = []
  pointpart_weld = PointPart.select().join(Point).join(Drawing).join(Order).where(PointPart.weld == 1,Order.cas == case,Point.faza == faza).group_by(PointPart.detail)
  for i in pointpart_weld:
    d.append((i.detail,1,1))
  Assembly_detail.insert_many(d, fields=[Assembly_detail.detail,Assembly_detail.assembly,Assembly_detail.weld]).execute()
  d = []
  pointpart_paint = PointPart.select().join(Point).join(Drawing).join(Order).where(Order.cas == case,Point.faza == faza).group_by(PointPart.detail)
  for i in pointpart_paint:
    d.append((i.detail,1))
  Paint_detail.insert_many(d, fields=[Paint_detail.detail,Paint_detail.paint]).execute()