import csv
from tekla import Size, Test
from models import Bolt, Drawing, Nut, Order, Washer, Weld, WeldNorm, Part as Parts, Point
from datetime import datetime
from db import connection
from operator import itemgetter
from tekla2 import TeklaAdd
from correction import PointCorrect


def Audit(xls,case,correct):
  error = {'error':0,'ASSEMBLY':[],'PART':[],'others':[],'area':[],'count':[],'weld':[],'bolt':[],'nut':[],'weight':[],'washer':[]}
  add = {}
  tekla = Tekla(xls)
  if isinstance(tekla,str):
    error['others'].append(tekla)
    error['error'] += 1
    PrintError(error,add,tekla,case)
    return error
  sql = Sql(case)
  if isinstance(sql,str):
    error['others'].append(sql)
    error['error'] += 1
    PrintError(error,add,tekla,case)
    return error
  for i in sql.keys():
    try:
      if round(sql[i]['area'],1) != round(tekla[i]['area'],1):
        error['error'] += 1
        error['area'].append(f'Площадь марки {i} изменилась')
        error['area'].append(sql[i]['area'])
        error['area'].append(tekla[i]['area'])
        error['area'].append('++++++++++++++++++++++++++')
    except:
      error['others'].append(f'{i} Такай марки нет в файле')
      error['error'] += 1
      PrintError(error,add,tekla,case)
      return error

    if sql[i]['count'] > tekla[i]['count']:
      error['error'] += 1
      error['count'].append(f'Количество марки {i} уменьшилось')

    if sql[i]['weld'] != tekla[i]['weld']:
      error['error'] += 1
      error['weld'].append(f'Длина сварки  {i} изменилась')
      error['weld'].append(sql[i]['weld'])
      error['weld'].append(tekla[i]['weld'])
      error['weld'].append('++++++++++++++++++++++++++')
      if correct:
        ReconWeld(i,tekla[i]['weld'])
        print('Weld')
      
    if sorted(sql[i]['bolt'],key=itemgetter('profile')) != sorted(tekla[i]['bolt'],key=itemgetter('profile')):
      error['error'] += 1
      error['bolt'].append(f'Болты {i} изменились')
      if correct:
        ReconB(i,tekla[i]['bolt'])
        print('B')

    if sorted(sql[i]['nut'],key=itemgetter('profile')) != sorted(tekla[i]['nut'],key=itemgetter('profile')):
      error['error'] += 1
      error['nut'].append(f'Гайки {i} изменились')
      if correct:
        ReconN(i,tekla[i]['nut'])
        print('N')

    if sorted(sql[i]['washer'],key=itemgetter('profile')) != sorted(tekla[i]['washer'],key=itemgetter('profile')):
      error['error'] += 1
      error['washer'].append(f'Шайбы {i} изменились')
      if correct:
        ReconW(i,tekla[i]['washer'])
        print('W')
    # print(i)
    if sql[i]['weight'] != tekla[i]['weight']:
      error['error'] += 1
      error['weight'].append(f'Вес марки {i} изменился')
      error['weight'].append(sql[i]['weight'])
      error['weight'].append(tekla[i]['weight'])
      error['weight'].append('++++++++++++++++++++++++++')

    if sorted(sql[i]['point'],key=itemgetter('point_z')) != sorted(tekla[i]['point'],key=itemgetter('point_z')):
      assembly = Assembly(i,tekla[i]['point'],sql[i]['point'],tekla[i]['count'],add,correct)
      if len(assembly) != 0:
        error['ASSEMBLY'].append(assembly)
        error['error'] += 1

  part = Part(tekla,sql)
  if len(part) != 0:
    error['error'] += 1
    error['PART'] = part

  for i in sql.keys():
    tekla.pop(i)
  return PrintError(error,add,tekla,case)


def PrintError(error,add,tekla,case):
  if error['error'] > 0:
    print(f'Количество ошибок: {error["error"]}')
    for e in error.keys():
      if e != 'error' and len(error[e]) != 0:
        for i in error[e]:
          print(i)
    return error
  else:
    print('OK')
    TeklaAdd(add,tekla,case)
    return error
            

      
def Assembly(mark,tekla,sql,count,add,correct):
  assembly = []
  s = sql.copy()
  t = tekla.copy()
  for y in sql:
    if len(t) != 0:
      try:
        t.remove(y)
        s.remove(y)
      except:
        pass
  if len(s) == 0 and len(t) == 0:
    pass
  elif len(s) != 0 and len(t) != 0:
    assembly.append(f'{mark} сборка изменилась')
    assembly.append(f'{s} сборка изменилась')
    assembly.append(f'{t} сборка изменилась')
    if correct:
      PointCorrect(mark,t,s)
  elif len(s) != 0:
    assembly.append(f'В файле отсутствуют сборки {mark} {s}')
  elif len(t) != 0:
    if len(sql) + len(t) == count:
      print(f'ОШИБКА {mark}')
      add[mark] = {}
      add[mark]['assembly'] = t
      add[mark]['count'] = count
    else:
      assembly.append(f'{mark} Количество сборок не соответствует')
  return assembly


def Tekla(xls):
  tekla = {}
  with open(xls,'r', encoding='windows-1251',newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[3].replace(' ','') == '1' and row[0].replace(' ','') == 'DRAWING' and row[1].replace(' ','').find('(?)') == -1:
        tekla[row[1].replace(' ','')] = {
          'area':float(row[4].replace(' ','')),
          'count':int(row[5].replace(' ','')),
          'part':{},
          'point':[],
          'weld':[],
          'bolt':[],
          'nut':[],
          'washer':[],
          'weight_clear': float(row[6].replace(' ','')),
        }
      if row[0].replace(' ','') == 'ASSEMBLY' and row[1].replace(' ','') in tekla.keys():
        try:
          if row[7].replace(' ','') == '':
            draw = None
          else:
            draw = str(row[7].replace(' ',''))
        except:
          draw = None
        if draw == None:
          return (f"нет номера чертежа {row[1].replace(' ','')}")
        tekla[row[1].replace(' ','')]['point'].append({
          'point_x':row[3].replace(' ','').replace('<','').replace('>','').split('/')[0].split('-')[0],
          'point_y':row[3].replace(' ','').replace('<','').replace('>','').split('/')[-1].split('-')[0],
          'point_z':float(row[2].replace(' ','')),
          'name':row[5].strip(),
          'draw':draw
        })
      if row[0].replace(' ','') == 'PART' and row[1].replace(' ','') in tekla.keys():
        if row[9].find('резина') != -1:
          profile_size = row[4].replace(' ','').replace('-','Резина')
        else:
          profile_size = row[4].replace(' ','')

        profile = Size(profile_size)
        if profile == None:
          return f"Новая номенклатура {row[4].replace(' ','')}"
        tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))] = {
          'count':int(row[3].replace(' ','')),
          'profile':profile[0],
          'size':profile[1],
          'length':float(row[5].replace(' ','')),
          'weight':float(row[6].replace(' ','')),
          'mark':row[8].replace(' ',''),
          'manipulation':row[9].replace(' ',''),
          'work':profile[2],
          'width':profile[3],
          'perimeter':int(Test(row[11].replace(' ',''))),
          'depth':float(Test(row[12].replace(' ',''),profile[1])),
          'area':float(row[13].replace(' ','')),
          'hole':[],
          'chamfer':{},
        }
        if (row[9].replace(' ','')).find('d') != -1:
          for hol in row[9].split(','):
            if hol.find('d') != -1:
              hol = hol.replace('d','').replace(' ','')
              tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['hole'].append({
                'diameter':int(hol[:2]),
                'count':(int(hol[-1])),
                'depth': 10
                })
      if row[0].replace(' ','') == 'WEIGHT' and row[1].replace(' ','') in tekla.keys():
        if row[3].replace(' ','') != '':
          more = 0
          more = float(row[3].replace(' ','').split(';')[1])
        else:
          more = 0
        tekla[row[1].replace(' ','')]['weight'] = {
          'weight':float(row[2].replace(' ','')),
          'more':more,
        }
        if tekla[row[1].replace(' ','')]['weight_clear'] - (tekla[row[1].replace(' ','')]['weight']['weight'] - tekla[row[1].replace(' ','')]['weight']['more']) > 2:
          return (f"слишком большая погрешность в весе {row[1].replace(' ','')}")
        elif tekla[row[1].replace(' ','')]['weight_clear'] - (tekla[row[1].replace(' ','')]['weight']['weight'] - tekla[row[1].replace(' ','')]['weight']['more']) < -2:
          return (f"слишком большая погрешность в весе {row[1].replace(' ','')}")


      if row[0].replace(' ','') == 'WELD' and row[1].replace(' ','') in tekla.keys():
        if WeldNorm.select().where(WeldNorm.cathet == int(float(row[2].replace(' ','')))) != None:
          if int(float(row[2].replace(' ',''))) == 0:
            cathet = 100
          else:
            cathet = int(float(row[2].replace(' ','')))
          tekla[row[1].replace(' ','')]['weld'].append({
            'cathet': cathet,
            'length':int(float(row[3].replace(' ','')) / tekla[row[1].replace(' ','')]['count']),
            'count':int(int(row[4].replace(' ','')) / tekla[row[1].replace(' ','')]['count'])
          })

      if row[0].replace(' ','') == 'BOLT' and row[1].replace(' ','') in tekla.keys():
        tekla[row[1].replace(' ','')]['bolt'].append({
          'profile':row[2].replace(' ',''),
          'gost':row[3].replace(' ',''),
          'count':int(int(row[4].replace(' ','')) / tekla[row[1].replace(' ','')]['count']),
          'weight':float(row[5].replace(' ',''))
        })
      if row[0].replace(' ','') == 'NUT' and row[1].replace(' ','') in tekla.keys():
        tekla[row[1].replace(' ','')]['nut'].append({
          'profile':row[2].replace(' ',''),
          'gost':row[3].replace(' ',''),
          'count':int(int(row[4].replace(' ','')) / tekla[row[1].replace(' ','')]['count']),
          'weight':float(row[5].replace(' ',''))
        })
      if row[0].replace(' ','') == 'WASHER' and row[1].replace(' ','') in tekla.keys():
        tekla[row[1].replace(' ','')]['washer'].append({
          'profile':row[2].replace(' ',''),
          'gost':row[3].replace(' ',''),
          'count':int(int(row[4].replace(' ','')) / tekla[row[1].replace(' ','')]['count']),
          'weight':float(row[5].replace(' ',''))
        })
      if row[0].replace(' ','') == 'HOLE' and row[1].replace(' ','') in tekla.keys():
        if row[6].replace(' ','') == '32484.3' or row[6].replace(' ','') == '52644':
          tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['hole'].append({
            'diameter':int(row[3].replace(' ','')),
            'count':(int(row[4].replace(' ','')))/tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['count'],
            'depth':int(row[5].replace(' ','')) / 2
          })

        
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) <= 8 and int(row[3].replace(' ','')) >= 14:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 10 and int(row[3].replace(' ','')) >= 19:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 12 and int(row[3].replace(' ','')) >= 23:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 14 and int(row[3].replace(' ','')) >= 23:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 16 and int(row[3].replace(' ','')) >= 23:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 18 and int(row[3].replace(' ','')) >= 30:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 20 and int(row[3].replace(' ','')) >= 35:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 22 and int(row[3].replace(' ','')) >= 35:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 25 and int(row[3].replace(' ','')) >= 40:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) >= 30 and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) <= 50 and int(row[3].replace(' ','')) >= 45:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 60 and int(row[3].replace(' ','')) >= 50:
          pass
        elif tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['profile'] == 'Лист' and int(tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['size']) == 80 and int(row[3].replace(' ','')) >= 100:
          pass
        else:
          tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['hole'].append({
            'diameter':int(row[3].replace(' ','')),
            'count':(int(row[4].replace(' ','')))/tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['count'],
            'depth':int(row[5].replace(' ','')) / 2
          })
      if row[0].replace(' ','') == 'CHAMFER' and row[1].replace(' ','') in tekla.keys():
        tekla[row[1].replace(' ','')]['part'][int(row[2].replace(' ',''))]['chamfer'] = {
          'length':float(row[3].replace(' ',''))
        }

  return tekla



def Sql(case):
  sql = {}
  for row in Drawing.select().join(Order).where(Order.cas == case):
    sql[row.assembly] = {
      'area':float(row.area),
      'count':row.count,
      'part':{},
      'point':[],
      'weld':[],
      'bolt':[],
      'nut':[],
      'washer':[],
      'weight':{'weight':float(row.weight),'more':float(row.more)}
    }
    for point in row.points:
      if point.draw == None:
        point.draw = ''
        return (f"нет номера чертежа {row.assembly}")
      sql[row.assembly]['point'].append({
        'point_x':point.point_x,
        'point_y':point.point_y,
        'point_z':float(point.point_z),
        'name':point.name,
        'draw':point.draw
      })
    for weld in row.welds:
      sql[row.assembly]['weld'].append({
        'cathet':weld.cathet.cathet,
        'length':int(weld.length),
        'count':weld.count
      })
    for bolt in row.bolts:
      sql[row.assembly]['bolt'].append({
        'profile':bolt.profile,
        'gost':bolt.gost,
        'count':int(bolt.count),
        'weight':float(bolt.weight)
      })
    for nut in row.nuts:
      sql[row.assembly]['nut'].append({
        'profile':nut.profile,
        'gost':nut.gost,
        'count':int(nut.count),
        'weight':float(nut.weight)
      })
    for washer in row.washers:
      sql[row.assembly]['washer'].append({
        'profile':washer.profile,
        'gost':washer.gost,
        'count':int(washer.count),
        'weight':float(washer.weight)
      })
    for part in row.parts:
      if part.number in sql[row.assembly]['part'].keys():
        sql[row.assembly]['part'][str(part.number)+' '+str(datetime.now())] = {
          'count':int(part.count),
          'profile':part.profile,
          'size':part.size,
          'length':float(part.length),
          'weight':float(part.weight),
          'mark':part.mark,
          'manipulation':part.manipulation,
          'work':part.work,
          'width':part.width,
          'perimeter':int(part.perimeter),
          'depth':float(part.depth),
          'area':float(part.area),
          'hole':[],
          'chamfer':{},
        }
      else:
        sql[row.assembly]['part'][part.number] = {
          'count':int(part.count),
          'profile':part.profile,
          'size':part.size,
          'length':float(part.length),
          'weight':float(part.weight),
          'mark':part.mark,
          'manipulation':part.manipulation,
          'work':part.work,
          'width':part.width,
          'perimeter':int(part.perimeter),
          'depth':float(part.depth),
          'area':float(part.area),
          'hole':[],
          'chamfer':{},
        }
      for hole in part.holes:
        sql[row.assembly]['part'][part.number]['hole'].append({
          'diameter':int(hole.diameter),
          'count':hole.count,
          'depth':hole.depth
        })
      for chamfer in part.chamfers:
        sql[row.assembly]['part'][part.number]['chamfer'] = {
          'length':float(chamfer.length)
        }

  return sql
  


def Part(tekla,sql):
  part = []
  delta = [
    ('count','Количество'),
    ('profile','Профиль'),
    ('size','Размер'),
    ('length','Длина'),
    ('weight','Вес'),
    ('mark','Марка'),
    ('manipulation','Операции'),
    ('work','В работе'),
    ('width','Ширина'),
    ('area','Площадь'),
    ('perimeter','Периметер'),
    ('depth','Глубина'),
    ('chamfer','Фаска'),
  ]
  corr = {'delete':[],'update':[],'error':[],'create':[]}
  for s in sql.keys():
    try:
      tekla[s]['part']
    except:
      corr['error'].append(s)
      break

    if sql[s]['part'] != tekla[s]['part']:
      aa = sql[s]['part'].copy()
      bb = tekla[s]['part'].copy()
      for a in sql[s]['part']:
        try:
          if aa[a] == bb[a]:
            del aa[a]
            del bb[a]
        except:
          pass
      for a in aa:
        if bb.get(a) == None:
          corr['delete'].append((s,a))
          # pr = Part.select().join(Drawing).where(Drawing.assembly == s,Part.number == a).first()
          # Hole.delete().where(Hole.part == pr).execute()
          # Chamfer.delete().where(Chamfer.part == pr).execute()
          # PointPart.delete().where(PointPart.part == pr).execute()
          # TaskPart.delete().where(TaskPart.part == pr).execute()
          # Part.delete().where(Part.id == pr).execute()
        else:
          corr['update'].append((s,a,aa.get(a),bb.get(a)))
          # pr = Part.select().join(Drawing).where(Drawing.assembly == s,Part.number == a).first()
          # pr.count = bb[a]['count']
          # pr.profile = bb[a]['profile']
          # pr.size = bb[a]['size']
          # pr.length = bb[a]['length']
          # pr.weight = bb[a]['weight']
          # pr.mark = bb[a]['mark']
          # pr.manipulation = bb[a]['manipulation']
          # pr.work = bb[a]['work']
          # pr.width = bb[a]['width']
          # pr.perimeter = bb[a]['perimeter']
          # pr.depth = bb[a]['depth']
          # pr.save()
          del bb[a]
      if bb != {}:
        corr['create'].append((s,bb))
  
  for i in corr['delete']:
    part.append(f'Удалена деталь № {i[1]} марки {i[0]}')
  for i in corr['update']:
    for d in delta:
      if i[2][d[0]] != i[3][d[0]]:
        part.append(f'Марка {i[0]} деталь {i[1]} {d[1]} В базе: {i[2][d[0]]}, В файле: {i[3][d[0]]}')
        # if d[1] == 'Площадь' and i[2][d[0]] == 0:
        #   drawing = Drawing.get(Drawing.assembly == i[0])
        #   Parts.update({Parts.area:i[3][d[0]]}).where(Parts.assembly == drawing,Parts.number == i[1]).execute()
  for i in corr['create']:
    for y in i[1]:
      part.append(f'Добавлена новая деталь № {y} к марке {i[0]}')

  return part
      

def ReconN(mark,tekla):
  dates = datetime.today()
  create = []
  delete = Drawing.get(Drawing.assembly == mark)
  Nut.delete().where(Nut.assembly == delete.id).execute()
  for y in tekla:
    create.append((delete,y['profile'],y['count'],y['gost'],y['weight'],dates))
  with connection.atomic():
    Nut.insert_many(create, fields=[Nut.assembly,Nut.profile,Nut.count,Nut.gost,Nut.weight,Nut.create_date]).execute()

def ReconW(mark,tekla):
  dates = datetime.today()
  create = []
  delete = Drawing.get(Drawing.assembly == mark)
  Washer.delete().where(Washer.assembly == delete.id).execute()
  for y in tekla:
    create.append((delete,y['profile'],y['count'],y['gost'],y['weight'],dates))
  with connection.atomic():
    Washer.insert_many(create, fields=[Washer.assembly,Washer.profile,Washer.count,Washer.gost,Washer.weight,Washer.create_date]).execute()

def ReconB(mark,tekla):
  dates = datetime.today()
  create = []
  delete = Drawing.get(Drawing.assembly == mark)
  Bolt.delete().where(Bolt.assembly == delete.id).execute()
  for y in tekla:
    create.append((delete,y['profile'],y['count'],y['gost'],y['weight'],dates))
  with connection.atomic():
    Bolt.insert_many(create, fields=[Bolt.assembly,Bolt.profile,Bolt.count,Bolt.gost,Bolt.weight,Bolt.create_date]).execute()

def ReconWeld(mark,tekla):
  dates = datetime.today()
  create = []
  delete = Drawing.get(Drawing.assembly == mark)
  Weld.delete().where(Weld.assembly == delete.id).execute()
  for y in tekla:
    create.append((delete,y['cathet'],y['length'],y['count'],dates))
  with connection.atomic():
    Weld.insert_many(create, fields=[Weld.assembly,Weld.cathet,Weld.length,Weld.count,Bolt.create_date]).execute()
