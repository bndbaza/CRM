import asyncio
from models import DetailUser, Drawing, Faza, Part, Point, PointPart, Task, TaskPart, User, Worker, Detail, Otc
from peewee import fn
import datetime
from db import connection
from send_bot import AllReport, Bots


def User_get(user):
  id = user.id
  user = user.user
  id = id.replace('\x10','').replace('\xad','').replace('\r','').lower().split(' ')[1]
  worker = Worker.select().where((Worker.id.in_([id,user])))
  if len(worker) == 2 and worker[0].oper != worker[1].oper:
    worker = Worker.select().where(Worker.id == id)
    user = None
  if user == '' or id == user:
    user = None
  base = Detail_result(id,worker,user,None)
  return base



def Detail_post(detail):
  users = detail.user
  detail = detail.detail.replace('\x10','').replace('\xad','').replace('\r','').lower().split(' ')
  if detail[0] == 'a':
    task = Detail.get(Detail.detail == detail[1],Detail.oper == users[0].oper)
    error,user2 = Detail_choise(task,users,task.to_work,True,'detail')
  elif detail[0] == 't':
    task = Task.get(Task.id == detail[1])
    user_list = []
    for user in users:
      user_list.append(user.id)
    try:
      one = Task.select(fn.MIN(Task.start).alias('min')).where((Task.worker_1.in_(user_list)) | (Task.worker_2.in_(user_list)),Task.end == None) 
      if (one[0].min + datetime.timedelta(days=1)) > datetime.datetime.today():
        time = True
      else:
        time = False
    except:
      time = True
    error,user2 = Detail_choise(task,users,1,time,'task')
  base = Detail_result(users[0].id,users,user2, error)
  return base



def Detail_result(id,worker,user,error):
  if worker[0].oper in ('assembly','weld','paint','set'):
    if user == None:
      detail = Detail.select().where((Detail.worker_1 == id)|(Detail.worker_2 == id),Detail.end == None)
    else:
      detail = Detail.select().where(Detail.worker_1.in_([id,user]),Detail.worker_2.in_([id,user]),Detail.end == None)
    if len(detail) == 0 and error == None:
      error = 'Список Пуст'
  else:
    if user == None:
      detail = Task.select().where((Task.worker_1 == id) | (Task.worker_2 == id),Task.end == None)
    else:
      detail = Task.select().where(Task.worker_1.in_([id,user]),Task.worker_2.in_([id,user]),Task.end == None)
    if len(detail) == 0 and error == None:
      error = 'Список Пуст'
  base = {'worker':list(worker),'detail':list(detail),'error':error}
  return base


def Detail_choise(task,users,to_work,one,stad):
  error = None
  user2 = None
  oper = None
  if task.oper == 'assembly':
    oper = 'set'
  elif task.oper == 'weld':
    oper = 'assembly'
  faza = task.faza
  dates = datetime.datetime.today()
  if to_work == 0:
    error = 'Предшедствующие операции не выполнены'
  elif task.end != None:
    error = 'Операция уже выполнена'
  elif users[0].oper in task.oper and str(users[0].id) in [str(task.worker_1),str(task.worker_2)]:
    error = Detail_close(task,dates,stad)
  elif one == False:
    error = 'Необходимо закончить задание'
  elif users[0].oper in task.oper and task.start == None:
    Detail_open(task,dates,faza,users,stad)
  elif oper != None and task.start == None:
    task_close = Detail.get(Detail.detail == task.detail,Detail.oper == oper)
    if task_close.start == None:
      error = 'Неверная операция'
    else: 
      error = Detail_close(task_close,dates,stad)
      if error == None:
        Detail_open(task,dates,faza,users,stad)
  else:
    error = 'Неверная операция'
  if len(users) == 2:
    task.worker_2 = users[1].id
    task.save()
    user2 = users[1].id
  return error, user2

def Task_end(task):
  # tp2 = TaskPart.select(TaskPart.part).join(Task).where(Task.end == None,Task.faza == task.faza).group_by(TaskPart.part).tuples()
  # tp = TaskPart.select(TaskPart.part).join(Task).where(TaskPart.part.not_in(tp2),Task.end != None,Task.faza == task.faza).tuples()
  # pp = PointPart.select(PointPart.detail).join(Point).join(Drawing).where(PointPart.part.not_in(tp),Point.faza == task.faza,Drawing.cas == task.order).group_by(PointPart.detail).tuples()
  # ppp = PointPart.select(PointPart.detail).join(Point).join(Drawing).where(PointPart.detail.not_in(pp),Point.faza == task.faza,Drawing.cas == task.order).group_by(PointPart.detail).tuples()
  # dd = Detail.select().where(Detail.detail.in_(ppp),Detail.oper == 'set',Detail.to_work == False)
  
  tp = TaskPart.select(TaskPart.part).join(Task).where(Task.end == None,Task.faza == task.faza,Task.order == task.order).tuples()
  pp = PointPart.select(PointPart.detail).join(Point).join(Drawing).where(PointPart.part.in_(tp),Point.faza == task.faza,Drawing.cas == task.order).group_by(PointPart.detail).tuples()
  dd = Detail.select().join(Faza).where(Detail.detail.not_in(pp),Detail.oper == 'set',Detail.to_work == False,Faza.faza == task.faza,Faza.case == task.order)
  
  
  print(len(tp),len(pp),len(dd))
  if len(dd) != 0:
    for d in dd:
      print(d.detail)
      d.to_work = True
    with connection.atomic():
      Detail.bulk_update(dd,fields=[Detail.to_work])
  faza = Faza.select().where(Faza.detail.not_in(pp),Faza.faza == task.faza,Faza.case == task.order)
  if len(faza) != 0:
    for i in faza:
      i.preparation = 3
      if i.set == 0:
        i.set = 1
    with connection.atomic():
      Faza.bulk_update(faza,fields=[Faza.preparation,Faza.set])


def Detail_end(task):
  opers = {'set':'assembly','assembly':'weld','weld':'paint'}
  try:
    detail = Detail.get(Detail.detail == task.detail,Detail.oper == opers[task.oper])
    if task.oper != 'weld':
      detail.to_work = True
    detail.save()
    faza = task.faza
    if task.oper == 'set':
      faza.set = 3
      faza.assembly = 1
    elif task.oper == 'assembly':
      faza.assembly = 3
      faza.weld = 1
    elif task.oper == 'weld':
      otc = Otc.select().where(Otc.detail == faza,Otc.oper == 'weld').first()
      if otc == None:
        otc = Otc.create(detail=faza,start=datetime.datetime.today(),oper='weld')
      else:
        otc.fix = 0
        otc.error += 1
        otc.save()
      worker = Worker.select(User.telegram).join(User).where(Worker.oper.in_(['otc'])).tuples()
      asyncio.run(AllReport(worker,f'{faza.detail} {task.worker_1.user.surname} Наряд на проверку сварки'))
      faza.weld = 3
      # faza.paint = 1
    faza.save()
  except:
    # Otc.get_or_create(detail=faza,start=datetime.datetime.today(),oper='weld')
    # otc = Worker.select(User.telegram).join(User).where(Worker.oper.in_(['admin'])).tuples()
    # AllReport(otc,f'{faza.detail} {detail.worker_1.user.surname} Наряд на проверку сварки')
    detail = Detail.select().where(Detail.detail == task.detail,Detail.oper == 'paint').first()
    if detail != None:
      detail.to_work = True
      detail.save()
      faza = task.faza
      faza.paint = 1
      faza.set = 3
      faza.assembly = 3
      faza.weld = 3
      faza.save()
    else:
      faza = task.faza
      otc = Otc.create(detail=faza,start=datetime.datetime.today(),oper='paint')
      faza.paint = 3
      faza.set = 3
      faza.assembly = 3
      faza.weld = 3
      faza.save()

    






def Detail_open(task,dates,faza,users,stad):
  task.start = dates
  task.worker_1 = users[0].id
  task.save()
  if stad == 'task':
    faza = Faza.select().where(Faza.faza == task.faza)
    if len(faza) != 0:
      for i in faza:
        i.in_work = 3
      with connection.atomic():
        Faza.bulk_update(faza,fields=[Faza.in_work])
    d = []
    for i in task.taskparts:
      d.append(i.part.id)
    pointpart = PointPart.select(PointPart.detail).join(Point).where(Point.faza == task.faza,PointPart.part.in_(d)).group_by(PointPart.detail).tuples()
    fazapp = Faza.select().where(Faza.detail.in_(pointpart))
    for i in fazapp:
      i.preparation = 2
    with connection.atomic():
        Faza.bulk_update(fazapp,fields=[Faza.preparation])
  elif stad == 'detail':
    if task.oper == 'set':
      faza.set = 2
    elif task.oper == 'assembly':
      faza.assembly = 2
    elif task.oper == 'weld':
      faza.weld = 2
    faza.save()

def Detail_close(task,dates,stad):
  error = None
  if dates - task.start <= datetime.timedelta(minutes=1):
    error = 'Прошло менее 30 минут'
  else:
    task.end = dates
    task.save()
    if stad == 'detail':
      if DetailUser.select().join(Detail).where(Detail.id == task.id).first() == None:
        data = []
        if task.worker_2 != None:
          data.append((task.id,task.worker_1,task.faza.weight / 2,task.norm / 2))
          data.append((task.id,task.worker_2,task.faza.weight / 2,task.norm / 2))
        else:
          data.append((task.id,task.worker_1,task.faza.weight,task.norm))
        print(data)
        with connection.atomic():
          DetailUser.insert_many(data,fields=[DetailUser.detail,DetailUser.worker,DetailUser.weight,DetailUser.norm]).execute()
      Detail_end(task)
    elif stad == 'task':
      Task_end(task)
  return error
