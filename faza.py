from models import Drawing, Order, Point, Part, PointPart
from db import connection
from peewee import fn, JOIN

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

def Test():
  z = Part.select(Part,fn.COUNT(Part.count).alias).join(Drawing)
  # print(z)
  for i in z:
    print(i.assembly)
