from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from db import connection
from models import Drawing, Order, Part, Point, Hole, Bolt, Nut, Washer, PointPart, Worker
from tekla import Tekla
from faza import Faza_update, PartPoint, Test, Faza_update_test, Detail_create, Faza_update_garage
from peewee import fn, JOIN
from schemas import OrderBase, DrawingBase, PointBase,PartBase, FazaBase, PointPartBase, WorkerBase
from task import Inf
from excel import NormExcel
from faza_list import Pdf, Inf_list
from qr import QRUser


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
def get_test():
  # PartPoint(1, '2313/3')
  # PartPoint(2, '2313/3')
  # PartPoint(4, '2313/3')
  # PartPoint(3, '2313/3')
  PartPoint(1, '2307')
  # Detail_create()
  return

@app.get('/excel')
def get_excel():
  NormExcel()
  return


@app.get('/pdf')
def get_pdf():
  z = [1]
  for y in z:
    case = '2307'
    detail = []
    if len(detail) == 0:
      faza = PointPart.select(PointPart.detail).join(Point).join(Drawing).join(Order).where(Point.faza == y,Order.cas == case).group_by(PointPart.detail)
      for i in faza:
        detail.append(i.detail)
    Inf(detail,case)
  return


@app.get('/list_faza')
def get_list_faza():
  case = '2313/3'
  faza = 1
  Inf_list(faza,case)
  return 


@app.post('/order')
def post_tekla(
  file: UploadFile = File(...),
  order: str = Form(...)
):
  Tekla(file,order)
  # Faza_update(order)
  # Faza_update_test(order)
  Faza_update_garage(order)
  return

@app.get('/worker/{id}',response_model=WorkerBase)
def get_detail(id):
  id = id.split(' ')[1]
  worker = Worker.select().where(Worker.id == id).first()
  return worker

@app.get('/qruser/{id}')
def get_qr_user(id):
  QRUser(id)
  return

@app.get('/delete')
def get_delete():
  
  return 