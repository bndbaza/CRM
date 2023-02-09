from excel import Statement,Cuting, Tag
from faza import PartPoint, Detail_create,Task_create
from models import Order,PointPart,Point,Drawing
from sawing_list import Sawing
from send_bot import Tech
from task import BaseInfo
from peewee import fn, Case
import asyncio


def PointPartInsert(lis,case):
  fazas = lis
  order = Order.get(Order.cas == case)
  for faza in fazas:
    PartPoint(faza,order)
    Detail_create(faza,order)
    Task_create(faza,order)
  weight_control(order)
  return



def PdfGenerate(lis,case):
  z = lis
  for y in z:
    case = case
    detail = []
    if len(detail) == 0:
      faza = PointPart.select(PointPart.detail).join(Point).join(Drawing).join(Order).where(Point.faza == y,Order.cas == case).group_by(PointPart.detail)
      for i in faza:
        detail.append(i.detail)
    asyncio.run(Tech(BaseInfo(detail,case)))
    asyncio.run(Tech(Statement(y,case)))
    asyncio.run(Tech(Cuting(y,case)))
    asyncio.run(Tech(Sawing(y,case)))
    asyncio.run(Tech(Tag(y,case)))
  return

def weight_control(order):
  weight_all = Point.select(Point.faza,fn.SUM(Drawing.weight).alias('weight')).join(Drawing).join(Order).where(Order.id == order.id).first()
  if order.weight < weight_all.weight:
    order.weight = weight_all.weight
    order.save()
