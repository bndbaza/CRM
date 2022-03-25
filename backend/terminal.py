from models import Drawing, Part, Point, PointPart, Task, TaskPart, Worker, Detail
import datetime
from db import connection

# def User_get(detail):
#   error = None
#   user = detail.user.replace('\x10','').replace('\xad','').replace('\r','').lower().split(' ')
#   print(user)
#   detail = detail.detail.replace('\x10','').replace('\xad','').replace('\r','').lower().replace('saw','saw_').split(' ')
#   worker = Worker.select().where(Worker.id == user).first()
#   d = Detail.select().where(Detail.detail == detail[1],Detail.oper == worker.oper).first()
#   if detail[0] != 'u':
#     print(detail,d,worker.oper)
#   if detail[0] != 'u' and d != None and d.basic == detail[2] and (d.worker == None or d.worker == worker):
#     error = Detail_post(d,worker)
#   elif detail[0] !='u':
#     error = 'Невозможно взять наряд'
#   job = Detail.select().where(Detail.worker_1 == worker,Detail.end == None)
#   if len(job) == 0 and error == None:
#     error = 'Список Пуст'
#   job = {'worker': list(job),'error':error}
#   return job


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
    error,user2 = Detail_choise(task,users,task.to_work,0)
  elif detail[0] == 't':
    task = Task.get(Task.task == detail[1])
    user_list = []
    for user in users:
      user_list.append(user.id)
    one = Task.select().where((Task.worker_1.in_(user_list)) | (Task.worker_2.in_(user_list)),Task.end == None)
    error,user2 = Detail_choise(task,users,1,len(one))
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


def Detail_choise(task,users,to_work,one):
  error = None
  user2 = None
  dates = datetime.datetime.today()
  if to_work == 0:
    error = 'Предшедствующие операции не выполнены'
  elif users[0].oper in task.oper and str(users[0].id) in [str(task.worker_1),str(task.worker_2)]:
    if dates - task.start <= datetime.timedelta(seconds=3):
      error = 'Прошло менее 5 минут'
    else:
      task.end = dates
      task.save()
      try:
        task.detail
        Detail_end(task)
      except:
        Task_end(task)
  elif one > 0:
    error = 'Необходимо закончить задание'
  elif users[0].oper in task.oper and task.start == None:
    task.start = dates
    task.worker_1 = users[0].id
    task.save()
  else:
    error = 'Неверная операция'
  if len(users) == 2:
    task.worker_2 = users[1].id
    user2 = users[1].id
  return error, user2

def Task_end(task):
  tp = TaskPart.select(TaskPart.part).join(Task).where(Task.end != None).tuples()
  pp = PointPart.select(PointPart.detail).join(Point).join(Drawing).where(PointPart.part.not_in(tp),Point.faza == task.faza,Drawing.cas == task.order).group_by(PointPart.detail).tuples()
  ppp = PointPart.select(PointPart.detail).join(Point).join(Drawing).where(PointPart.detail.not_in(pp),Point.faza == task.faza,Drawing.cas == task.order).group_by(PointPart.detail).tuples()
  dd = Detail.select().where(Detail.detail.in_(ppp),Detail.oper == 'set',Detail.to_work == False)
  if len(dd) != 0:
    for d in dd:
      d.to_work = True
    with connection.atomic():
      Detail.bulk_update(dd,fields=[Detail.to_work])


def Detail_end(task):
  opers = ['assembly','weld','paint']
  details = Detail.select().where(Detail.detail == task.detail,Detail.oper.in_(opers),Detail.to_work == False)
  for detail in details:
    if detail.oper == opers[0]:
      detail.to_work = True
      detail.save()
      break
    elif detail.oper == opers[1]:
      detail.to_work = True
      detail.save()
      break
    elif detail.oper == opers[2]:
      detail.to_work = True
      detail.save()
      break
    else:
      break



