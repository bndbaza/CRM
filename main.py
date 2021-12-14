from typing import List
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from db import connection
from models import Drawing, Order, Part, Point, Hole, Bolt, Nut, Washer
from tekla import Tekla
from faza import Faza_update
from peewee import fn, JOIN
from schemas import OrderBase, DrawingBase, PointBase,PartBase


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


@app.get('/')#,response_model=List[PointBase])
def get():
  point = Point.select(Point.faza,fn.SUM(Drawing.weight).alias('aaa')).join(Drawing).group_by(Point.faza)

  b = Bolt.select(Bolt.profile,fn.SUM(Bolt.weight * Bolt.count).alias('aaa'),Bolt.weight,fn.SUM(Bolt.count).alias('bbb')).group_by(Bolt.profile)

  n = Nut.select(Nut.profile,fn.SUM(Nut.weight * Nut.count).alias('aaa'),Nut.weight,fn.SUM(Nut.count).alias('bbb')).group_by(Nut.profile)

  w = Washer.select(Washer.profile,fn.SUM(Washer.weight * Washer.count).alias('aaa'),Washer.weight,fn.SUM(Washer.count).alias('bbb'),Washer.gost).group_by(Washer.gost)
  for i in w:
    print(i.aaa,i.weight,i.bbb,i.gost)
  return #point

# @app.post('/',response_model=Drawing)
# async def postDrawing(drawing: Drawing):
#   await drawing.save()
#   return drawing

@app.post('/order')
async def postTekla(
  file: UploadFile = File(...),
  order: str = Form(...)
):
  Tekla(file,order)
  Faza_update(order)
  return # await Point.objects.filter(assembly__cas__cas=order,faza=4).sum('assembly__weight')