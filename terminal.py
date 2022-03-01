from models import Drawing, Worker, Detail
import datetime

def User_get(detail):
  error = None
  user = detail.user.replace('\x10','').replace('\xad','').replace('\r','').lower().split(' ')
  detail = detail.detail.replace('\x10','').replace('\xad','').replace('\r','').lower().replace('saw','saw_').split(' ')
  worker = Worker.select().where(Worker.id == user[1]).first()
  d = Detail.select().where(Detail.detail == detail[1],Detail.oper == worker.oper).first()
  if detail[0] != 'u' and d != None and d.basic == detail[2] and (d.worker == None or d.worker == worker):
    error = Detail_post(d,worker)
  elif detail[0] !='u':
    error = 'Невозможно взять наряд'
  job = Detail.select().where(Detail.worker == worker,Detail.end == None)
  if len(job) == 0 and error == None:
    error = 'Список Пуст'
  job = {'worker': list(job),'error':error}
  return job

def Detail_post(b,worker):
  dates = datetime.datetime.today()
  error = None
  num = []
  details = Detail.select().where(Detail.detail == b.detail,Detail.end == None)
  for detail in details:
    if detail.oper != 'assembly' and detail.oper != 'weld' and detail.oper != 'paint':
      num.append('zag')
    else:
      num.append(detail.oper)
  print(num)
  if b.oper == 'paint' and len(num) == 1 and 'paint' in num:
    pass
  elif b.oper == 'weld' and 'assembly' not in num:
    pass
  elif b.oper == 'assembly' and 'zag' not in num:
    pass
  elif b.oper != 'assembly' and b.oper != 'weld' and b.oper != 'paint':
    pass
  else:
    error = 'Предшествующие операции не выполнены'
    return error
  if b.worker:
    if dates - b.start <= datetime.timedelta(seconds=300):
      error = 'Прошло менее 5 минут'
    else:
      pass
      b.end = dates
  else:
    pass
    b.start = dates
    b.worker = worker
  b.save()
  return error