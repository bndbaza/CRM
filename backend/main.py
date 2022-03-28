from email.encoders import encode_base64
from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from test import AAA
from db import connection
from models import *
from tekla import Tekla
from faza import Faza_update, PartPoint, Test, Faza_update_test, Detail_create, Faza_update_garage, Task_create
from peewee import fn, JOIN
from schemas import DetailBase1, OneDetailBase, OrderBase, DrawingBase, PointBase,PartBase, FazaBase, PointPartBase, WorkerBase, BasicDetailBase, DetailBase,BasicDetailBase1
from task import Inf
from excel import NormExcel, Statement, Cuting
from faza_list import Pdf, Inf_list
from qr import QRUser
from terminal import Detail_post, User_get
from qr_list import QR_pdf
from sawing_list import Sawing
from correction import Correction


app = FastAPI()


@app.on_event("startup")
def startup():
    connection.connect()

@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()

app.state.database = connection


origins = [
  "http://localhost",
  "http://127.0.0.1:8080",
  "http://192.168.0.75:8080",
  # "http://192.168.0.213:8080",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)




@app.get('/test')
def get_test():
  # Detail_create(1,'2325')
  # Detail_create(2,'2325')
  # Detail_create(3,'2325')
  # Detail_create(4,'2325')
  # Detail_create(5,'2325')
  # Detail_create(6,'2325')
  # Detail_create(7,'2325')
  # Detail_create(8,'2325')
  # order = Order.get(Order.cas == '2325')
  # Task_create(8,order)
  # Detail_create(9,'2325')
  Detail_create(8,'2325')
  # PartPoint(9,2325)
  # PartPoint(12,2325)
  return

@app.get('/excel')
def get_excel():
  NormExcel()
  return


@app.get('/pdf')
def get_pdf():
  z = [12]
  for y in z:
    case = '2325'
    detail = []
    if len(detail) == 0:
      faza = PointPart.select(PointPart.detail).join(Point).join(Drawing).join(Order).where(Point.faza == y,Order.cas == case).group_by(PointPart.detail)
      for i in faza:
        detail.append(i.detail)
    Inf(detail,case)
    Statement(y,'2325')
    Cuting(y,'2325')
  return


@app.get('/list_faza')
def get_list_faza():
  case = '2325'
  faza = 6
  Inf_list(faza,case)
  return 


@app.post('/order')
def post_tekla(
  file: UploadFile = File(...),
  order: str = Form(...)
):
  Tekla(file,order)
  Faza_update(order)
  # Faza_update_test(order)
  # Faza_update_garage(order)
  return

@app.get('/qruser/{id}')
def get_qr_user(id):
  QR_pdf()
  # QRUser(id)
  return

@app.get('/stat')
def get_stat():
  dd = Part.select(Part.number,fn.COUNT(fn.DISTINCT(Part.profile)).alias('aaa')).join(Drawing).join(Order).where(Order.cas == '2325').group_by(Part.number).having(fn.COUNT(fn.DISTINCT(Part.profile)) > 1)
  for d in dd:
    print(d.number,d.aaa)
  return



@app.get('/delete/{id}')
def get_qr_user(id):
  bolt = Drawing.select().where(Drawing.cas == id)
  Bolt.delete().where(Bolt.assembly.in_(bolt)).execute()
  Nut.delete().where(Nut.assembly.in_(bolt)).execute()
  Washer.delete().where(Washer.assembly.in_(bolt)).execute()
  Weld.delete().where(Weld.assembly.in_(bolt)).execute()
  chamfers = Part.select().where(Part.assembly.in_(bolt))
  Chamfer.delete().where(Chamfer.part.in_(chamfers)).execute()
  Hole.delete().where(Hole.part.in_(chamfers)).execute()
  PointPart.delete().where(PointPart.part.in_(chamfers)).execute()
  Part.delete().where(Part.assembly.in_(bolt)).execute()
  Point.delete().where(Point.assembly.in_(bolt)).execute()
  Drawing.delete().where(Drawing.cas == id).execute()
  Order.delete().where(Order.id == id).execute()
  return



@app.post('/worker',response_model=BasicDetailBase1)
def get_worker(user: DetailBase):
  connection.close()
  base = User_get(user)
  return base



@app.post('/details',response_model=BasicDetailBase1)
def get_details(detail: DetailBase1):
  job = Detail_post(detail)
  return job

@app.get('/task',response_model=List[BasicDetailBase])
def get_task():
  connection.close()
  go = Detail.select().where(Detail.to_work == True,Detail.end == None)
  return list(go)


@app.get('/weight')
def get_weight():
  weight = Point.select(Point.faza,fn.SUM(Drawing.weight).alias('weight')).join(Drawing).join(Order).where(Order.cas == '2325').group_by(Point.faza)
  for i in weight:
    print(i.faza,i.weight)

@app.get('/error')
def get_error():
  # a = Drawing.select(fn.MAX(Drawing.id).alias('_id'),Drawing.assembly,fn.COUNT(Drawing.assembly).alias('cou')).where(Drawing.cas == 15).group_by(Drawing.assembly).having(fn.COUNT(Drawing.assembly) > 1)
  # for i in a:
  #   print(i.assembly,i.cou,i._id)
    # Drawing.delete().where(Drawing.id == i._id).execute()
  # Detail.delete().where(Detail.id > 6000).execute()
  Detail.update({Detail.to_work: False, Detail.worker_1: None,Detail.worker_2: None,Detail.start: None,Detail.end:None}).execute()
  Task.update({Task.worker_1: None,Task.worker_2: None,Task.start: None,Task.end:None}).execute()

@app.get('/correction')
def get_correction():
  Correction()
  return

@app.get('/index',response_model=List[BasicDetailBase])
def get_index():
  index = Detail.select().where(Detail.to_work == True, Detail.end == None,Detail.basic.in_(['weld','set','paint']))
  return list(index)

@app.get('/detail/{id}',response_model=OneDetailBase)
def get_detail(id):
  pointparts = PointPart.select().where(PointPart.detail == id)
  pp = PointPart.select(Part.id).join(Part).join_from(PointPart,Point).where(PointPart.detail == id).tuples()
  details = Detail.select().where(Detail.detail == id,Detail.basic.in_(['weld','set','paint']))
  tasks = TaskPart.select().join(Task).where(TaskPart.part.in_(pp),Task.faza == pointparts[0].point.faza)
  return {'pointparts': list(pointparts), 'details':list(details), 'tasks':list(tasks)}

@app.get('/aaa')
def get_aaa():
  AAA()
