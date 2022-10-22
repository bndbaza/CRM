import shutil
from typing import List
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from audit import Audit
from package_list import PackList
from pdf_act_otc import ActEveryDay
from shipment_list import ShipmentList
from tekla3 import PdfGenerate, PointPartInsert
from test import AAA, ASS, BBB, CCC, CORRECT, DDD, DEDR, DELDEL, FOOD, GGG, HHH, HOLEC, HOLECOF, JJ, JKL, JN, KOZ, LLL, METALL, NNN, NORMSAW, PAINT, PIN, PL, PP, QWE, SAWCOF, SHIP, TEST, TTT, USS, UUU, WELDCOF, WELDCOR, WELDNORM, XXX, YYY, ZAE, ZZZ, rrr
from db import connection
from models import *
from tekla import Tekla
from faza import Faza_update, PartPoint, Test, Faza_update_test, Detail_create, Faza_update_garage, Task_create
from peewee import fn, JOIN, Case
from schemas import *
from task import BaseInfo
from excel import NormExcel, Statement, Cuting, Tag
from faza_list import Pdf, Inf_list
from qr import QRPack, QRRun, QRUser
from terminal import Detail_post, User_get
from qr_list import QR_pdf
from sawing_list import Sawing
from correction import Correction, Replace
from d_list import Dlist
from shipment import Start
import asyncio
from fastapi.responses import FileResponse
from test2 import PAINTNONE, NormPaint, Time, Time4, Time5, UserNorm
import operations

app = FastAPI()

@app.on_event("startup")
async def startup():
  connection.connect()
  task1 = asyncio.create_task(Start())

@app.on_event("shutdown")
def shutdown():
  if not connection.is_closed():
    connection.close()

app.state.database = connection

origins = [
  "http://localhost",
  "http://127.0.0.1:8080",
  "http://192.168.0.75:8080",
  "http://192.168.0.213:8080",
  "http://176.215.255.156:8080",
  "http://176.215.255.156:80",
  "http://176.215.255.156",
  "http://bndbaza.ru",
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
  fazas = [1]
  order = Order.get(Order.cas == '23256')
  for faza in fazas:
    if Faza.select().where(Faza.case == order,Faza.faza == faza).first() != None:
      print('УЖЕ ЕСТЬ')
      return
    PartPoint(faza,order)
    Detail_create(faza,order)
    Task_create(faza,order)
  connection.close()
  return

@app.get('/excel')
def get_excel():
  NormExcel()
  connection.close()
  return

@app.get('/pdf')
def get_pdf():
  z = [1]
  for y in z:
    case = '23504'
    detail = []
    if len(detail) == 0:
      faza = PointPart.select(PointPart.detail).join(Point).join(Drawing).join(Order).where(Point.faza == y,Order.cas == case).group_by(PointPart.detail)
      for i in faza:
        detail.append(i.detail)
    BaseInfo(detail,case)
    Statement(y,case)
    Cuting(y,case)
    Sawing(y,case)
    Tag(y,case)
  connection.close()
  return

@app.get('/index',response_model=List[OrderBase])
def get_index():
  orders = Order.select().where(Order.status != None)
  connection.close()
  return list(orders)

@app.get('/list_faza')
def get_list_faza():
  case = '2325'
  faza = 6
  Inf_list(faza,case)
  connection.close()
  return 

@app.post('/order')
def post_tekla(
  file: UploadFile = File(...),
  order: str = Form(...),
  correct: bool = Form(...)
):
  file_name = 'EXCEL/' + str(datetime.datetime.today()) + file.filename
  with open(file_name, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  if correct:
    result = Audit(file_name,order,True)
  result = Audit(file_name,order,False)
  if result['error'] == 0:
    if Point.select().join(Drawing).join(Order).where(Order.cas == order,Point.faza == None).first() != None:
      Faza_update(order)
      point = Point.select(Point.faza).join(Drawing).join(Order).where(Order.cas == order).group_by(Point.faza).tuples()
      pointpart = PointPart.select(Point.faza).join(Point).join(Drawing).join(Order).where(Order.cas == order).group_by(Point.faza).tuples()
      result = list(set(point) - set(pointpart))
      print(f'result {result}')
      try:
        result.remove(max(result))
      except:
        result = [max(point) + 1,]
      d = []
      for i in result:
        d.append(i[0])
      PointPartInsert(d,order)
      PdfGenerate(d,order)
  # Tekla(file,order)
  # Faza_update_test(order)
  # Faza_update_garage(order)
  connection.close()
  return result

@app.get('/qruser')
def get_qr_user():
  # weld = Worker.select(Worker.id).where(Worker.oper == 'weld').tuples()

  QR_pdf((210,))
  # QRUser(id)
  connection.close()
  return

@app.get('/stat')
def get_stat():
  # a = (1,2,3,4)
  # b = (1,5,3,6,2,4)
  # result = list(set(b) - set(a))
  # result.remove(max(result))
  QRRun(2183,'2325','weld')
  # for i in range(1,2):
  #   QRPack(i)
  # text = 'Привет'
  # asyncio.run(Bots(text))
  # await Bots(text)
  connection.close()
  return

@app.get('/delete/{id}')
def get_qr_user(id):
  drawing = Drawing.select().where(Drawing.cas == id)
  Bolt.delete().where(Bolt.assembly.in_(drawing)).execute()
  Nut.delete().where(Nut.assembly.in_(drawing)).execute()
  Washer.delete().where(Washer.assembly.in_(drawing)).execute()
  Weld.delete().where(Weld.assembly.in_(drawing)).execute()
  part = Part.select().where(Part.assembly.in_(drawing))
  Chamfer.delete().where(Chamfer.part.in_(part)).execute()
  Hole.delete().where(Hole.part.in_(part)).execute()
  TaskPart.delete().where(TaskPart.part.in_(part)).execute()
  Task.delete().where(Task.order == id).execute()
  pointpart = PointPart.select(PointPart.detail).where(PointPart.part.in_(part)).group_by(PointPart.detail).tuples()
  Detail.delete().where(Detail.detail.in_(pointpart)).execute()
  Faza.delete().where(Faza.detail.in_(pointpart)).execute()
  PointPart.delete().where(PointPart.part.in_(part)).execute()
  Part.delete().where(Part.assembly.in_(drawing)).execute()
  Point.delete().where(Point.assembly.in_(drawing)).execute()
  Drawing.delete().where(Drawing.cas == id).execute()
  Order.delete().where(Order.id == id).execute()
  connection.close()
  return

@app.post('/worker',response_model=BasicDetailBase1)
def get_worker(user: DetailBase):
  base = User_get(user)
  connection.close()
  return base

@app.post('/details',response_model=BasicDetailBase1)
def get_details(detail: DetailBase1):
  job = Detail_post(detail)
  connection.close()
  return job

@app.get('/task',response_model=TerminalBase)
def get_task():
  saw = Detail.select().where(Detail.faza != None).group_by(Detail.detail).having(fn.SUM(Detail.to_work) == 0)
  assembly = Detail.select().where(Detail.to_work == True,Detail.end == None)
  connection.close()
  return {'saw':list(saw),'assembly':list(assembly)}

@app.get('/weight/{id}')
def get_weight(id):
  weight = Point.select(Point.faza,fn.SUM(Drawing.weight).alias('weight')).join(Drawing).join(Order).where(Order.cas == id).group_by(Point.faza)
  for i in weight:
    print(i.faza,i.weight)
  connection.close()

@app.get('/error')
def get_error():
  # a = Drawing.select(fn.MAX(Drawing.id).alias('_id'),Drawing.assembly,fn.COUNT(Drawing.assembly).alias('cou')).where(Drawing.cas == 15).group_by(Drawing.assembly).having(fn.COUNT(Drawing.assembly) > 1)
  # for i in a:
  #   print(i.assembly,i.cou,i._id)
    # Drawing.delete().where(Drawing.id == i._id).execute()
  # Detail.delete().where(Detail.id > 6000).execute()
  Detail.update({Detail.to_work: False, Detail.worker_1: None,Detail.worker_2: None,Detail.start: None,Detail.end:None}).execute()
  Task.update({Task.worker_1: None,Task.worker_2: None,Task.start: None,Task.end:None}).execute()
  connection.close()

@app.get('/correction')
def get_correction():
  # mark = ['КБ-3','КБ-4','КБ-5','КБ-6','КБ-11','КБ-12','КБ-14','КБ-19','КБ-21','КБ-22','КБ-23','КБ-24','КБ-25','КБ-26','КБ-27','КБ-28','КБ-30','КБ-31','КБ-32','КК-1','КК-2','КК-3','КК-6','КОг-11','КР-1','КСв-9','КШ-1']
  mark = ['ЛОг-31','ЛОг-32','ЛОг-36','ЛОг-38','ЛОг-38','ЛБ-6','ЛН-1','ЛБ-7']
  order = '23501'
  order = Order.get(Order.cas == order)
  for m in mark:
    Correction(m,order)
  # Replace()
  connection.close()
  return

@app.get('/stage/{id}')#,response_model=List[StageBase])
def get_stage(id):
  # index1 = Detail.select(Detail.id).where(Detail.to_work == True, Detail.end == None,Detail.basic.in_(['weld','set','paint'])).tuples()
  # index2 = Detail.select(Detail.id).where(Detail.to_work == False,Detail.basic == 'set').tuples()
  # index = Detail.select().where(Detail.id.in_(index1) | Detail.id.in_(index2)).order_by(Detail.detail)
  # return list(index)
  stage = []
  if id == '0':
    # stage.append({'name':'Заготовка','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.set == 0).order_by(Faza.detail).dicts())})
    stage.append({'name':'Заготовка','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.set == 0).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Готов к комплектации','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.set == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'Готов к комплектации','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.set == 1).order_by(Faza.detail).dicts())})
    # stage.append({'name':'В комплектации','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.set == 2).order_by(Faza.detail).dicts())})
    stage.append({'name':'В комплектации','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.set == 2).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Готов к сборке','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.assembly == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'Готов к сборке','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.assembly == 1).order_by(Faza.detail).dicts())})
    # stage.append({'name':'В сборке','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.assembly == 2).order_by(Faza.detail).dicts())})
    stage.append({'name':'В сборке','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.assembly == 2).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Готов к сварке','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.weld == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'Готов к сварке','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.weld == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'В сварке','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.weld == 2).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Ожидает ОТК после сварки','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.weld == 3,Faza.paint == 0).order_by(Faza.detail).dicts())})
    stage.append({'name':'Ожидает ОТК после сварки','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.weld == 3,Faza.paint == 0).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Готов к покраске','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.paint == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'Готов к покраске','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.paint == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'В покраске','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.paint == 2).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Ожидает ОТК после покраски','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.paint == 3,Faza.packed == 0).order_by(Faza.detail).dicts())})
    stage.append({'name':'Ожидает ОТК после покраски','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.paint == 3,Faza.packed == 0).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Готов к упаковке','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.packed == 1).order_by(Faza.detail).dicts())})
    stage.append({'name':'Готов к упаковке','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.packed == 1).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Упакован','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.packed == 3,Faza.shipment == 0).order_by(Faza.detail).dicts())})
    stage.append({'name':'Упакован','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.packed == 3,Faza.shipment == 0).order_by(Faza.detail).dicts())})
    # stage.append({'name':'Отгружен','faza':list(Faza.select(Faza,Order.color.alias('color'),Otc.fix).join(Order).join_from(Faza,Otc,JOIN.LEFT_OUTER).where(Order.status == 'В работе',Faza.shipment == 3).order_by(Faza.detail).dicts())})
    stage.append({'name':'Отгружен','faza':list(Faza.select(Faza,Order.color.alias('color')).join(Order).where(Order.status == 'В работе',Faza.shipment == 3).order_by(Faza.detail).dicts())})
  elif id.split(',')[1].isdigit():
    id = id.split(',')
    stage = Faza.select(Faza).join(Order).where(Order.status == 'В работе',Order.cas == id[0],Faza.faza == id[1]).dicts()
  else:
    id = id.split(',')
    if id[0] != '0':
      pp = PointPart.select(PointPart.detail).join(Part).join(Drawing).join(Order).where(Order.cas == id[0],Drawing.assembly == id[1]).group_by(PointPart.detail).tuples()
      stage = Faza.select(Faza).join(Order).where(Order.status == 'В работе',Faza.detail.in_(pp)).dicts()
      print(len(stage))
    else:
      pp = PointPart.select(PointPart.detail).join(Part).join(Drawing).where(Drawing.assembly == id[1]).group_by(PointPart.detail).tuples()
      stage = Faza.select(Faza).join(Order).where(Order.status == 'В работе',Faza.detail.in_(pp)).dicts()

  connection.close()
  return list(stage)

@app.get('/detail/{id}',response_model=OneDetailBase)
def get_detail(id):
  pointparts = PointPart.select().where(PointPart.detail == id)
  pp = PointPart.select(Part.id).join(Part).join_from(PointPart,Point).where(PointPart.detail == id).tuples()
  details = Detail.select().where(Detail.detail == id,Detail.basic.in_(['weld','set','paint']))
  tasks = TaskPart.select().join(Task).where(TaskPart.part.in_(pp),Task.faza == pointparts[0].point.faza)
  pack = DetailPack.select().join(Faza).where(Faza.detail == id).first()
  if pack:
    pack = pack.pack
  connection.close()
  return {'pointparts': list(pointparts), 'details':list(details), 'tasks':list(tasks), 'pack':pack}

@app.get('/aaa')
def get_aaa():
  # AAA()
  # BBB()
  # CCC()
  # XX()
  # DDD()
  # EEE()
  # GGG()
  # HHH()
  # RRR()
  # Audit()
  # YYY()
  # ZZZ()
  # UUU()
  # USS()
  # Time()result * 
  ASS()
  # CORRECT()
  # DELDEL()
  # TEST()
  # PAINT()
  # Time()
  # UserNorm()
  # Time4()
  # FAZAS()
  # NormPaint()
  # DEDR()
  # WELDCOR()
  # WELDNORM()
  # METALL()
  # NORMSAW()
  # SHIP()
  # KOZ()
  # WELDCOF()
  # HOLECOF()
  # JKL()
  # PIN()
  # PAINTNONE()
  # Time5()
  # HOLEC()
  # SAWCOF()
  # TTT()
  # JN()
  # JJ()
  connection.close()

#############################################  Молярка Не востребовано  ##########################################################
# @app.get('/paint/{detail}',response_model=BasicDetailBase2)
# def get_paint(detail):
#   date = datetime.datetime.today()
#   d = []
#   details = detail.split(',')
#   for i in details:
#     d.append(i.split(' ')[1])
#   in_job = Detail.select().where(Detail.start == None,Detail.oper == 'paint',Detail.detail.in_(d),Detail.to_work == 2)
#   from_job = Detail.select().join(Worker).where(Detail.start != None,Detail.end == None,Detail.oper == 'paint',Detail.detail.in_(d),Worker.id == 92)
#   no_job = Detail.select().where(Detail.start == None,Detail.oper == 'paint',Detail.detail.in_(d),Detail.to_work == 0)
#   connection.close()
#   return {'in_job':list(in_job),'from_job':list(from_job),'no_job':list(no_job)}

# @app.post('/inpaint')
# def post_inpaint(ppp:BasicDetailBase2):
#   date = datetime.datetime.today()
#   d = []
#   details = []
#   for id in ppp.in_job:
#     d.append(id.id)
#     details.append(id.detail)
#   Detail.update({Detail.start: date,Detail.worker_1: 92}).where(Detail.id.in_(d)).execute()
#   Faza.update({Faza.paint: 2}).where(Faza.detail.in_(details)).execute()
#   connection.close()
#   return

# @app.post('/outpaint')
# def post_outpaint(ppp:BasicDetailBase2):
#   date = datetime.datetime.today()
#   d = []
#   details = []
#   for id in ppp.in_job:
#     d.append(id.id)
#     details.append(id.detail)
#   Detail.update({Detail.end: date}).where(Detail.id.in_(d)).execute()
#   Faza.update({Faza.paint: 3,Faza.packed: 1}).where(Faza.detail.in_(details)).execute()
#   connection.close()
#   return
######################################################################################################################################

@app.get('/report/faza/{order}')#,response_model=List[FazaReport])
def get_report_faza(order):
  order = Order.get(Order.cas == order)
  faza = Faza.select(
    Faza.faza,
    fn.SUM(Faza.weight).alias('weight_kmd'),
    fn.SUM(Case(None,[(Faza.in_work == 3,Faza.weight)],0)).alias('weight_in_work'),
    fn.SUM(Case(None,[(Faza.preparation == 3,Faza.weight)],0)).alias('weight_preparation'),
    fn.SUM(Case(None,[(Faza.set == 3,Faza.weight)],0)).alias('weight_set'),
    fn.SUM(Case(None,[(Faza.assembly == 3,Faza.weight)],0)).alias('weight_assembly'),
    fn.SUM(Case(None,[(Faza.weld == 3,Faza.weight)],0)).alias('weight_weld'),
    fn.SUM(Case(None,[(Faza.paint == 3,Faza.weight)],0)).alias('weight_paint'),
    fn.SUM(Case(None,[(Faza.packed == 3,Faza.weight)],0)).alias('weight_packed'),
    fn.SUM(Case(None,[(Faza.shipment == 3,Faza.weight)],0)).alias('weight_shipment'),
    fn.SUM(Case(None,[(Faza.in_object == 3,Faza.weight)],0)).alias('weight_in_object'),
    fn.SUM(Case(None,[(Faza.mount == 3,Faza.weight)],0)).alias('weight_mount'),
  ).where(Faza.case == order).group_by(Faza.faza).dicts()

  case = Faza.select(
    Faza.faza,
    fn.SUM(Faza.weight).alias('weight_kmd'),
    fn.SUM(Case(None,[(Faza.in_work == 3,Faza.weight)],0)).alias('weight_in_work'),
    fn.SUM(Case(None,[(Faza.preparation == 3,Faza.weight)],0)).alias('weight_preparation'),
    fn.SUM(Case(None,[(Faza.set == 3,Faza.weight)],0)).alias('weight_set'),
    fn.SUM(Case(None,[(Faza.assembly == 3,Faza.weight)],0)).alias('weight_assembly'),
    fn.SUM(Case(None,[(Faza.weld == 3,Faza.weight)],0)).alias('weight_weld'),
    fn.SUM(Case(None,[(Faza.paint == 3,Faza.weight)],0)).alias('weight_paint'),
    fn.SUM(Case(None,[(Faza.packed == 3,Faza.weight)],0)).alias('weight_packed'),
    fn.SUM(Case(None,[(Faza.shipment == 3,Faza.weight)],0)).alias('weight_shipment'),
    fn.SUM(Case(None,[(Faza.in_object == 3,Faza.weight)],0)).alias('weight_in_object'),
    fn.SUM(Case(None,[(Faza.mount == 3,Faza.weight)],0)).alias('weight_mount'),
  ).where(Faza.case == order).group_by(Faza.case).dicts().first()
  case['faza'] = 'Итог'
  faza = list(faza)
  faza.append(case)
  connection.close()
  return {'faza':faza}

@app.get('/report/all/{order}',response_model=AllReport)
def get_report_all(order):
  order = Order.get(Order.cas == order)
  faza = Faza.select(
    fn.SUM(Faza.weight).alias('weight_kmd'),
    fn.SUM(Case(None,[(Faza.in_work == 3,Faza.weight)],0)).alias('weight_in_work'),
    fn.SUM(Case(None,[(Faza.paint != 0,Faza.weight)],0)).alias('weight_weld'),
    fn.SUM(Case(None,[(Faza.paint == 3,Faza.weight)],0)).alias('weight_paint'),
    fn.SUM(Case(None,[(Faza.packed == 3,Faza.weight)],0)).alias('weight_packed'),
    fn.SUM(Case(None,[(Faza.shipment == 3,Faza.weight)],0)).alias('weight_shipment'),
    fn.SUM(Case(None,[(Faza.mount == 3,Faza.weight)],0)).alias('weight_mount'),
  ).where(Faza.case == order).group_by(Faza.case).first()
  faza.weight_order = order.weight
  connection.close()
  return faza

@app.get('/dlist')
def get_dlist():
  Dlist()
  # CalcDlist()
  connection.close()

@app.get('/report/workers/assembly/{start}/{end}',response_model=List[DetailUserBase])
def get_report_user(start,end):
  end = end.split('-')
  end = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),23,59,59)
  dua = DetailUser.select(DetailUser,fn.SUM(DetailUser.weight).alias('weight_all'),fn.SUM(DetailUser.norm).alias('norm_all')).join(Detail).join(Faza).join_from(DetailUser,Worker).where(Detail.oper == 'assembly',Detail.end >= start,Detail.end <= end).group_by(DetailUser.worker)
  for i in dua:
    x = round(i.norm_all)
    h = int(x / 60)
    m = str(x - (h * 60))
    if len(m) == 1:
      m = '0'+m
    i.norm_all = str(h)+':'+m
  connection.close()
  return list(dua)

@app.get('/report/workers/paint/{start}/{end}')
def get_report_user(start,end):
  end = end.split('-')
  end = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),23,59,59)
  paints = []
  users = Worker.select().where((Worker.oper == 'paint') | (Worker.oper == 'master'))
  for user in users:
    detail = Detail.select(fn.SUM(Case(None,[(Detail.worker_2 != None,Detail.norm / 2)],Detail.norm))).where((Detail.worker_1 == user) | (Detail.worker_2 == user),Detail.end != None,Detail.end > start,Detail.end < end ).scalar()
    if detail != None:
      detail = (str(detail).split('.')[0])
      paints.append({'user':user.user,'norm':detail})
  return list(paints)

@app.get('/report/workers/weld/{start}/{end}',response_model=List[DetailUserBase])
def get_report_weld_user(start,end):
  end = end.split('-')
  end = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),23,59,59)
  duw = DetailUser.select(DetailUser,fn.SUM(DetailUser.weight).alias('weight_all')).join(Detail).join(Faza).join_from(DetailUser,Worker).where(Detail.oper == 'weld',Detail.end >= start,Detail.end < end).group_by(DetailUser.worker)
  for i in duw:
    d = DetailUser.select(Detail.detail).join(Detail).where(DetailUser.worker == i.worker,Detail.end >= start,Detail.end < end).tuples()
    d2 = DetailUser.select(Detail.detail).join(Detail).where(DetailUser.worker == i.worker,Detail.end >= start,Detail.end < end,Detail.worker_2 != None).tuples()
    pp = PointPart.select(PointPart.point).where(PointPart.detail.in_(d)).group_by(PointPart.point).tuples()
    # pp3 = PointPart.select(PointPart.point).where(PointPart.detail.in_(d)).group_by(PointPart.point)
    pp1 = PointPart.select(PointPart.point).where(PointPart.detail.in_(d2)).group_by(PointPart.point).tuples()
    pp2 = []
    for pr in pp1:
      pp2.append(pr[0])
    welds = Weld.select(Weld,fn.SUM(Case(None,[(Point.id.in_(pp2),Weld.length/2)],Weld.length)).alias('lenn')).join(Drawing).join(Point).where(Point.id.in_(pp)).group_by(Weld.cathet)
    i.weld = []
    index = 0
    for weld in welds:
      # cathet = WeldNorm.get(WeldNorm.cathet == weld.cathet)
      cathet = weld.cathet
      x = weld.lenn / 1000 * cathet.norm
      index += x
      i.weld.append({'cathet': weld.cathet,'length': weld.lenn})
    norm = round(index)
    h = int(norm / 60)
    m = str(norm - (h * 60))
    if len(m) == 1:
      m = '0'+m
    i.norm_all = str(h)+':'+m
  connection.close()
  return list(duw)

@app.get('/package_get/{id}',response_model=List[PackedBase])
def get_package(id):
  packs = Packed.select().join(Order).where(Order.cas == id)
  connection.close()
  return list(packs)

@app.get('/package_delete/{id}/{case}',response_model=List[PackedBase])
def delete_pack(id,case):
  dp = DetailPack.select(DetailPack.detail).where(DetailPack.pack == id)
  for d in dp:
    d = d.detail
    d.packed = 1
    d.save()
  DetailPack.delete().where(DetailPack.pack == id).execute()
  Packed.delete().where(Packed.id == id).execute()
  packs = Packed.select().join(Order).where(Order.cas == case)
  connection.close()
  return list(packs)

@app.post('/package_post',response_model=List[PackedBase])
def post_package(pack:PackedBaseAll):
  pack = pack.pack
  pac = Packed.get(Packed.id == pack.id)
  ready = PackList(pack)
  pac.size = pack.size
  pac.pack = pack.pack
  pac.ready = ready
  pac.save()
  dp = DetailPack.select(DetailPack.detail).where(DetailPack.pack == pac)
  for d in dp:
    d = d.detail
    d.packed = 3
    d.save()
  packs = Packed.select().join(Order).where(Order.cas == pack.order.cas)
  connection.close()
  return list(packs)

@app.get('/file/{id}')
def files(id):
  files = Packed.get(Packed.id == id)
  connection.close()
  return FileResponse(files.ready)

@app.get('/register/{id}')
def get_register(id):
  point = Point.select(Drawing.assembly,Drawing.weight,fn.COUNT(Drawing.assembly).alias('count'),fn.SUM(Drawing.weight).alias('weight_all')).join(Drawing).join(Order).where(Order.cas == id).group_by(Drawing.assembly).dicts()
  p = Point.select(fn.COUNT(Order.id).alias('count')).join(Drawing).join(Order).where(Order.cas == id).group_by(Order.cas == id).scalar()
  drawing = Drawing.select(fn.COUNT(Order.cas == id).alias('count')).join(Order).where(Order.cas == id).group_by(Order.cas == id).scalar()

  # w = Point.select(fn.SUM(Drawing.weight)).join(Drawing).join(Order).where(Order.cas == id).scalar()
  # ff = Faza.select(Faza,fn.COUNT(Faza.detail).alias('ccc')).join(Order).where(Order.cas == id).group_by(Faza.detail)
  # pp = PointPart.select(PointPart).join(Point).join(Drawing).join(Order).where(Order.cas == id).group_by(PointPart.detail).order_by(Drawing.assembly)
  # for x in pp:
  #   f = Faza.get(Faza.detail == x.detail)
  #   if x.point.assembly.weight != f.weight and x.point.assembly.assembly.find('Ш-') == -1:
  #     f.weight = x.point.assembly.weight
  #     f.save()
  #     print(x.detail,x.point.assembly.assembly,x.point.assembly.weight,f.weight)


  connection.close()
  return {'all':{'drawing':drawing,'count':p},'point':list(point)}

@app.get('/act_everyday/{today}')
def get_act_everyday(today):
  today = today.split('-')
  today = datetime.date(int(today[0]),int(today[1]),int(today[2]))
  weld = ActEveryDay(today,'weld')
  paint = ActEveryDay(today,'paint')
  connection.close()
  return {'weld': weld, 'paint': paint}

@app.get('/act/file/{id}')
def files(id):
  id = id.replace('z',' ')
  connection.close()
  return FileResponse(f'media/acts/atc{id}.pdf')

@app.get('/package_structure/{id}',response_model=List[PointPartBase])
def structure_package(id):
  pack = DetailPack.select(Faza.detail).join(Packed).join_from(DetailPack,Faza).where(Packed.number == id).tuples()
  pp = PointPart.select(PointPart,fn.COUNT(Part.id).alias('count')).join(Part).join(Drawing).where(Drawing.cas == 15,PointPart.detail.in_(pack)).group_by(PointPart.detail)
  detail = PointPart.select().where(PointPart.detail.in_(pack)).group_by(PointPart.detail)
  for p in detail:
    print(p.detail,p.part.assembly.assembly)
  connection.close()
  return list(detail)

@app.get('/get_cars/{id}',response_model=List[ShipmentBase])
def get_cars(id):
  cars = Shipment.select(Shipment).join_from(Shipment,Order).where(Order.cas == id)
  connection.close()
  return list(cars)

@app.post('/post_car',response_model=List[ShipmentBase])
def post_car(car:CarPostBase):
  car = car.car
  order = Order.get(Order.cas == car.case)
  if Shipment.select(fn.MAX(Shipment.number)).scalar() == None:
    drive = 1
  else:
    drive = Shipment.select(fn.MAX(Shipment.number)).scalar() + 1
  Shipment.create(order=order,number=drive,car=car.car,number_car=car.number_car,driver=car.driver)
  cars = Shipment.select().join(Order).where(Order.cas == car.case)
  connection.close()
  return list(cars)

@app.get('/close_ship/{id},{case}',response_model=List[ShipmentBase])
def close_ship(id,case):
  ship = ShipmentList(id)
  car = Shipment.get(Shipment.id == id)
  car.ready = ship
  car.save()
  detail = DetailPack.select(Faza.detail).join(Packed).join_from(DetailPack,Faza).where(Packed.shipment == car).tuples()
  Faza.update({Faza.shipment:3}).where(Faza.detail.in_(detail)).execute()
  cars = Shipment.select(Shipment).join_from(Shipment,Order).where(Order.cas == case)
  connection.close()
  return list(cars)

@app.get('/file_ship/{id}')
def files(id):
  files = Shipment.get(Shipment.id == id)
  connection.close()
  return FileResponse(files.ready)


@app.get('/users')
def users():
  oper = ['admin','shipment','master','otc','chief','director']
  users = User.select().join(Worker).where(Worker.oper.not_in(oper)).order_by(User.surname).group_by(User.id).dicts()
  connection.close()
  return list(users)

@app.get('/report/user/{id}/{start}/{end}')
def report_user(id,start,end):
  # end = end.split('-')
  # end = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),23,59,59)
  # user = Worker.select().where(Worker.user == id)
  # res = {}
  # for work in user:
  #   if work.oper != 'paint':
  #     # details = Detail.select(Detail,Faza).join(Faza).where((Detail.worker_1 == work.id) | (Detail.worker_2 == work.id),Detail.end > start, Detail.end < end).dicts()
  #     details = DetailUser.select(DetailUser.norm,DetailUser.weight,Detail,Faza).join(Detail).join(Faza).where(DetailUser.worker == work.id,Detail.end > start, Detail.end < end).dicts()
  #     details = list(details)
  #     # result = Detail.select(Detail,Faza,fn.SUM(Detail.norm).alias('sum_norm'),fn.SUM(Faza.weight).alias('sum_weight')).join(Faza).where((Detail.worker_1 == work.id) | (Detail.worker_2 == work.id),Detail.end > start, Detail.end < end).group_by().dicts().first()
  #     result = DetailUser.select(Detail,Faza,fn.SUM(DetailUser.norm).alias('sum_norm'),fn.SUM(DetailUser.weight).alias('sum_weight')).join(Detail).join(Faza).where(DetailUser.worker == work.id,Detail.end > start, Detail.end < end).group_by().dicts().first()
  #     if len(details) != 0:
  #       for detail in details:
  #         pp = PointPart.select().where(PointPart.detail == detail['detail']).first()
  #         detail['mark'] = pp.point.assembly.assembly
  #         detail['draw'] = pp.point.draw
  #         detail['name'] = pp.point.name
  #       result['norm'] = result['sum_norm']
  #       result['weight'] = result['sum_weight']
  #       result['detail'] = 'Итог'
  #       details.append(result)
  #       res[work.oper_rus] = details
  # for work in user:
  #   if work.oper == 'paint':
  #     details = Detail.select(Detail,Faza).join(Faza).where((Detail.worker_1 == work.id) | (Detail.worker_2 == work.id),Detail.end > start, Detail.end < end).dicts()
  #     details = list(details)
  #     result = Detail.select(Detail,Faza,fn.SUM(Detail.norm).alias('sum_norm'),fn.SUM(Faza.weight).alias('sum_weight')).join(Faza).where((Detail.worker_1 == work.id) | (Detail.worker_2 == work.id),Detail.end > start, Detail.end < end).group_by().dicts().first()
  #     if len(details) != 0:
  #       for detail in details:
  #         pp = PointPart.select().where(PointPart.detail == detail['detail']).first()
  #         detail['mark'] = pp.point.assembly.assembly
  #         detail['draw'] = pp.point.draw
  #         detail['name'] = pp.point.name
  #       result['norm'] = result['sum_norm']
  #       result['weight'] = result['sum_weight']
  #       result['detail'] = 'Итог'
  #       details.append(result)
  #     res[work.oper_rus] = details
  # for work in user:
  #   if work.oper != 'hole' and work.oper != 'saw' and work.oper != 'bevel':
  #     details = Task.select(Task,TaskPart,Part,fn.SUM(TaskPart.count).alias('count_all')).join(TaskPart).join(Part).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).dicts()
  #     details = list(details)
  #     if len(details) != 0:
  #       # for detail in details:
  #       #   detail.part = detail.taskparts[0].part
  #       # result['norm'] = result['sum_norm']
  #       # result['weight'] = result['sum_weight']
  #       res[work.oper_rus] = details
  #   if work.oper == 'saw':
  #     details = Task.select(Task,TaskPart,Part,fn.SUM(TaskPart.count).alias('count_all')).join(TaskPart).join(Part).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).dicts()
  #     details = list(details)
  #     norm_all = 0
  #     if len(details) != 0:
  #       for detail in details:
  #         norm = SAWCOF(detail['profile'],detail['area'],detail['count_all'] + 2)
  #         norm_all += norm
  #         detail['norm'] = norm
  #       details.append({'task':'Итог','norm':norm_all})
  #       res[work.oper_rus] = details
  #   if work.oper == 'bevel':
  #     details = Task.select(Task,TaskPart,Part,fn.SUM(TaskPart.count).alias('count_all')).join(TaskPart).join(Part).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).dicts()
  #     details = list(details)
  #     norm_all = 0
  #     if len(details) != 0:
  #       for detail in details:
  #         norm = SAWCOF(detail['profile'],detail['area'],detail['count_all'] + 2,1.5)
  #         norm_all += norm
  #         detail['norm'] = norm
  #       details.append({'task':'Итог','norm':norm_all})
  #       res[work.oper_rus] = details
  #   elif work.oper == 'hole':
  #     # details = Task.select(Task,fn.SUM(Hole.count * TaskPart.count * HoleNorm.norm).alias('count')).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where(Task.oper == 'hole',Task.id == t.id).group_by(Hole.diameter,Hole.depth)
  #     details = Task.select(fn.SUM(Hole.count * TaskPart.count * HoleNorm.norm).alias('norm'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task,Part).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).dicts()
  #     result = Task.select(fn.SUM(Hole.count * TaskPart.count * HoleNorm.norm).alias('norm'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).dicts().first()
  #     details = list(details)
  #     if len(details) != 0:
  #       # for detail in details:
  #       #   detail.part = detail.taskparts[0].part
  #       result['task'] = 'Итог'
  #       details.append(result)
  #       res[work.oper_rus] = details
  res = operations.Operation(id,start,end)
  connection.close()
  return res

@app.get('/fazas/{case}')
def fazas(case):
  faza = Point.select(Point.faza).join(Drawing).join(Order).where(Order.cas == case).group_by(Point.faza).tuples()
  connection.close()
  return list(faza)

@app.get('/metall/{case}/{faza}')
def metall(case,faza):
  pp = PointPart.select(Part.profile,Part.size,Part.mark,fn.SUM(Part.weight * Part.count).alias('weight')).join(Part).join(Drawing).join(Order).join_from(PointPart,Point).where(Order.cas == case,Point.faza == faza).group_by(Part.profile,Part.size,Part.mark).dicts()
  connection.close()
  return list(pp)

@app.get('/ip')
def ip(request:Request):
  host = request.client.host
  user = User.select().where(User.ip == host).dicts().first()
  connection.close()
  return user