from models import Drawing, Order, Point, Part, PointPart
from db import connection

def Faza_update(order):
  post = []
  # points = Point.filter(assembly__cas__cas = order).order_by(Point.point_z,Point.point_y,Point.point_x)
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

def PartPoint():
  parts = Part.select()
  # points = Point.select().where(Point.faza == 1)
  points = Point.filter(faza = 1)
  all = []
  for point in points:
    for part in parts:
      if point.assembly == part.assembly:
        d = (point,part)
        all.append(d)
  with connection.atomic():
    PointPart.insert_many(all, fields=[PointPart.point,PointPart.part]).execute()
