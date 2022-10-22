import datetime
from models import *
from peewee import fn, Case

def Operation(id,start,end):
  end = end.split('-')
  end = datetime.datetime(int(end[0]),int(end[1]),int(end[2]),23,59,59)
  user = Worker.select().where(Worker.user == id)
  res = {}
  for work in user:
    if work.oper != 'paint':
      details = DetailUser.select(DetailUser.id,DetailUser.norm,DetailUser.weight,Detail,Faza).join(Detail).join(Faza).where(DetailUser.worker == work.id,Detail.end > start, Detail.end < end).order_by(Detail.end).dicts()
      print(len(details))
      details = list(details)
      result = DetailUser.select(Detail,Faza,fn.SUM(DetailUser.norm).alias('sum_norm'),fn.SUM(DetailUser.weight).alias('sum_weight')).join(Detail).join(Faza).where(DetailUser.worker == work.id,Detail.end > start, Detail.end < end).group_by().dicts().first()
      if len(details) != 0:
        for detail in details:
          print(detail['id'],detail['detail'],detail['oper'])
          pp = PointPart.select().where(PointPart.detail == detail['detail']).first()
          detail['mark'] = pp.point.assembly.assembly
          detail['draw'] = pp.point.draw
          detail['name'] = pp.point.name
        result['norm'] = result['sum_norm']
        result['weight'] = result['sum_weight']
        result['detail'] = 'Итог'
        details.append(result)
        res[work.oper_rus] = details
  for work in user:
    if work.oper == 'paint':
      details = Detail.select(Detail,Faza).join(Faza).where((Detail.worker_1 == work.id) | (Detail.worker_2 == work.id),Detail.end > start, Detail.end < end).order_by(Detail.end).dicts()
      details = list(details)
      result = Detail.select(Detail,Faza,fn.SUM(Detail.norm).alias('sum_norm'),fn.SUM(Faza.weight).alias('sum_weight')).join(Faza).where((Detail.worker_1 == work.id) | (Detail.worker_2 == work.id),Detail.end > start, Detail.end < end).group_by().dicts().first()
      if len(details) != 0:
        for detail in details:
          pp = PointPart.select().where(PointPart.detail == detail['detail']).first()
          detail['mark'] = pp.point.assembly.assembly
          detail['draw'] = pp.point.draw
          detail['name'] = pp.point.name
        result['norm'] = result['sum_norm']
        result['weight'] = result['sum_weight']
        result['detail'] = 'Итог'
        details.append(result)
      res[work.oper_rus] = details
  for work in user:
    if work.oper != 'hole' and work.oper != 'saw' and work.oper != 'bevel':
      details = Task.select(Task,TaskPart,Part,fn.SUM(TaskPart.count).alias('count_all')).join(TaskPart).join(Part).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).order_by(Task.end).dicts()
      details = list(details)
      if len(details) != 0:
        res[work.oper_rus] = details
    elif work.oper == 'saw':
      details = Task.select(Task,TaskPart,Part,fn.SUM(TaskPart.count).alias('count_all')).join(TaskPart).join(Part).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).order_by(Task.end).dicts()
      details = list(details)
      norm_all = 0
      if len(details) != 0:
        for detail in details:
          norm = SAWCOF(detail['profile'],detail['area'],detail['count_all'] + 2)
          norm_all += norm
          detail['norm'] = norm
        details.append({'task':'Итог','norm':norm_all})
        res[work.oper_rus] = details
    elif work.oper == 'bevel':
      details = Task.select(Task,TaskPart,Part,fn.SUM(TaskPart.count).alias('count_all')).join(TaskPart).join(Part).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).order_by(Task.end).dicts()
      details = list(details)
      norm_all = 0
      if len(details) != 0:
        for detail in details:
          print(detail)
          norm = SAWCOF(detail['profile'],detail['area'],detail['count_all'] + 2,1.5)
          norm_all += norm
          detail['norm'] = norm
        details.append({'task':'Итог','norm':norm_all})
        res[work.oper_rus] = details
    elif work.oper == 'hole':
      # details_1 = Task.select(fn.SUM(Hole.count * TaskPart.count * HoleNorm.norm).alias('norm'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task,Part).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end,Part.profile != 'Лист').group_by(Task).dicts()
      details_1 = Task.select(fn.SUM(Hole.count * TaskPart.count * Case(None,[(Part.profile == 'Лист',HoleNorm.norm * 2.5 * 0.4)],HoleNorm.norm * 2.5)).alias('norm'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task,Part).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).group_by(Task).order_by(Task.end).dicts()
      # details_2 = Task.select(fn.SUM(Hole.count * TaskPart.count * HoleNorm.norm).alias('norm'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task,Part).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end,Part.profile == 'Лист').group_by(Task).dicts()
      # details_2 = Task.select(fn.SUM(Hole.count * HoleNorm.norm).alias('norm_part'),fn.SUM(TaskPart.count).alias('norm_task_part'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task,Part).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end,Part.profile == 'Лист').group_by(Task).dicts()
      # details_2 = HoleSheet(details_2)
      result = Task.select(fn.SUM(Hole.count * TaskPart.count * Case(None,[(Part.profile == 'Лист',HoleNorm.norm * 2.5 * 0.4)],HoleNorm.norm * 2.5)).alias('norm'),fn.SUM(Hole.count * TaskPart.count).alias('count'),Task).join(TaskPart).join(Part).join(Hole).join(HoleNorm).where((Task.worker_1 == work.id) | (Task.worker_2 == work.id),Task.end > start, Task.end < end).dicts().first()
      details = list(details_1)#+list(details_2)
      if len(details) != 0:
        result['task'] = 'Итог'
        result['end'] = ''
        details.append(result)
        res[work.oper_rus] = details
  return res

def SAWCOF(profile,S,count,bevel=1):
  print(profile)
  if profile == 'Двутавр':
    S_min,S_max,t_min,t_max = (10.32,187,2,25)
  if profile == 'Уголок':
    S_min,S_max,t_min,t_max = (1.47,78,0.7,15)
  if profile == 'Швеллер':
    S_min,S_max,t_min,t_max = (7.51,61,1.8,11)
  if profile == 'Труба круглая':
    S_min,S_max,t_min,t_max = (1.42,163,0.7,20)
  if profile == 'Труба профильная':
    S_min,S_max,t_min,t_max = (0.34,113,0.5,17)
  if profile == 'Круг':
    S_min,S_max,t_min,t_max = (0.79,707,0.8,40)
  if profile == 'Арматура':
    S_min,S_max,t_min,t_max = (0.79,707,0.8,40)

  S = float(S)
  result = t_min-(((t_min-t_max)/100)*((100/(S_max-S_min))*(S-S_min)))
  return result * int(count) * bevel

def HoleSheet(details):
  for detail in details:
    print(detail['norm_task_part'] * detail['norm_part'])
    norm = 100 // detail['depth']
    print(norm)
    norm = detail['norm_task_part'] // norm + 1
    print(norm,detail['norm_task_part'])
    norm_one = norm * detail['norm_part']
    print(norm_one,detail['norm_part'])
    norm_two = (detail['norm_task_part'] - norm) * detail['depth']
    print(norm_two)
    norm_two = int(norm_two) * 0.04
    print(norm_two)
    norm = float(norm_one) + float(norm_two)
    print(norm)
    detail['norm'] = norm
    print('-------------------------------------------------')





  return details