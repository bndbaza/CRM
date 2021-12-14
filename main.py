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

  b = Bolt.select(fn.SUM(Bolt.weight * Bolt.count).alias('aaa'))

  n = Nut.select(fn.SUM(Nut.weight * Nut.count).alias('aaa'))
  w = Washer.select(fn.SUM(Washer.weight * Washer.count).alias('aaa'))
  print(n.scalar() + b.scalar() + w.scalar())
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