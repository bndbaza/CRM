from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from db import connection
from models import Drawing, Order, Part, Point, Hole, Bolt, Nut, Washer, PointPart
from tekla import Tekla
from faza import Faza_update, PartPoint
from peewee import fn, JOIN
from schemas import OrderBase, DrawingBase, PointBase,PartBase, FazaBase
from report import Pdf, Inf


app = FastAPI()
app.state.database = connection


origins = [
  "http://localhost",
  "http://127.0.0.1:8080",
  "http://192.168.0.75:8080",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# @app.get('/',response_model=List[PartBase])
# def get():
#   point = Point.select(Point.faza,fn.SUM(Drawing.weight).alias('aaa')).join(Drawing).group_by(Point.faza)
#   w = Point.select(Point.assembly).where(Point.faza == 1)
#   d = Part.select().where(fn.Substr(Part.profile, 1, 1) != '-',Part.assembly.in_(w))
#   for i in d:
#     print(i.assembly, i.profile, i.length, i.count)
#   return list(d)


@app.get('/test')
def gettest():
  PartPoint(1, '2313/1')
  return


@app.get('/pdf')
def getPdf():
  case = '2313/1'
  detail = [6,8]
  if len(detail) == 0:
    faza = PointPart.select(PointPart.detail).join(Point).join(Drawing).join(Order).where(Point.faza == 1,Order.cas == case).group_by(PointPart.detail)
    for i in faza:
      detail.append(i.detail)
  # print(faza[0].detail)
  Inf(detail,case)
  return


# @app.get('/test2')
# def gettest2():
#   query = PointPart.select(PointPart,Part,Point).join_from(PointPart,Part).join_from(PointPart,Point).where(fn.Substr(Part.profile, 1, 1) != '-').order_by(Point.line)
#   for i in query:
#     print(i.point.assembly,i.part.profile,i.point.line)
#   return 


@app.post('/order')
async def postTekla(
  file: UploadFile = File(...),
  order: str = Form(...)
):
  Tekla(file,order)
  Faza_update(order)
  return