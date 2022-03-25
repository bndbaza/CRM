import csv
from datetime import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.styles.numbers import BUILTIN_FORMATS
from models import *
from peewee import fn
from tekla import Size,Test
from db import connection


def AAA():
  er = 'МК-2'
  drawing = {'DRAWING':[],'ASSEMBLY':[],'PART':[],'WEIGHT':[],'WELD':[],'BOLT':[],'NUT':[],'WASHER':[],'HOLE':[],'CHAMFER':[]}
  post = {'Drawing': [],'Point':[],'Part':[],'Weld':[],'Bolt':[],'Nut':[],'Washer':[],'Hole':[],'Chamfer':[],'Weight':[]}
  with open('BSS.xls','r', encoding='windows-1251',newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[1].replace(' ','') == er:
        d = []
        for i in row:
          d.append(i.replace(' ',''))
        drawing[row[0].replace(' ','')].append(d)
  pp = PointPart.select().join(Point).join(Drawing).join(Order).where(Drawing.assembly == er)
  point = pp[0].point
  detail = pp[0].detail
  col = Drawing.get(Drawing.assembly == er)
  PointPart.delete().where(PointPart.detail == detail).execute()
  Weld.delete().where(Weld.assembly == col).execute()
  Bolt.delete().where(Bolt.assembly == col).execute()
  Nut.delete().where(Nut.assembly == col).execute()
  Washer.delete().where(Washer.assembly == col).execute()
  part_d = Part.select(Part.id).where(Part.assembly == col).tuples()
  Hole.delete().where(Hole.part.in_(part_d)).execute()
  Chamfer.delete().where(Chamfer.part.in_(part_d)).execute()
  Part.delete().where(Part.assembly == col).execute()

  dates = datetime
  for i in drawing['PART']:
    profile = Size(i[4])
    post['Part'].append((col,
                int(i[2]),
                int(i[3]),
                profile[0],
                profile[1],
                float(i[5]),
                float(i[6]),
                i[8],
                i[9],
                profile[2],
                profile[3],
                int(Test(i[11])),
                float(Test(i[12],profile[1])),
                dates))
  


  with connection.atomic():
    Part.insert_many(post['Part'], fields=[Part.assembly,
                                  Part.number,
                                  Part.count,
                                  Part.profile,
                                  Part.size,
                                  Part.length,
                                  Part.weight,
                                  Part.mark,
                                  Part.manipulation,
                                  Part.work,
                                  Part.width,
                                  Part.perimeter,
                                  Part.depth,
                                  Part.create_date]).execute()
  
  

  for i in drawing['WELD']:
    post['Weld'].append((col,float(i[2]),float(i[3]),int(i[4]),dates))

  for i in drawing['BOLT']:
    post['Bolt'].append((col,i[2],i[3],int(i[4]),float(i[5]),dates))


  for i in drawing['NUT']:
    post['Nut'].append((col,i[2],i[3],int(i[4]),float(i[5]),dates))

  
  for i in drawing['WASHER']:
    post['Washer'].append((col,i[2],i[3],int(i[4]),float(i[5]),dates))

  

  for i in drawing['HOLE']:
    part = Part.get(number=int(i[2]),assembly=col)
    if part.profile == 'Лист' and int(part.size) < 14:
      pass
    else:
      post['Hole'].append((part,int(i[3]),(int(i[4]))/part.count,int(i[5]) / 2,dates))

  for i in drawing['CHAMFER']:
    part = Part.get(number=int(i[2]),assembly=col)
    post['Chamfer'].append((part,float(i[3]),dates))



  with connection.atomic():
    Weld.insert_many(post['Weld'], fields=[Weld.assembly,Weld.cathet,Weld.length,Weld.count,Weld.create_date]).execute()
    Bolt.insert_many(post['Bolt'], fields=[Bolt.assembly,Bolt.profile,Bolt.gost,Bolt.count,Bolt.weight,Bolt.create_date]).execute()
    Nut.insert_many(post['Nut'], fields=[Nut.assembly,Nut.profile,Nut.gost,Nut.count,Nut.weight,Nut.create_date]).execute()
    Washer.insert_many(post['Washer'], fields=[Washer.assembly,Washer.profile,Washer.gost,Washer.count,Washer.weight,Washer.create_date]).execute()
    Hole.insert_many(post['Hole'], fields=[Hole.part,Hole.diameter,Hole.count,Hole.depth,Hole.create_date]).execute()
    Chamfer.insert_many(post['Chamfer'], fields=[Chamfer.part,Chamfer.length,Chamfer.create_date]).execute()

  w = drawing['WEIGHT'][0]
  if w[3] != '':
    more = 0
    more = float(w[3].split(';')[1])
  else:
    more = 0
  col.weight = float(w[2]),
  col.more=more,
  post['Weight'].append(col)
  with connection.atomic():
    Drawing.bulk_update(post['Weight'], fields=[Drawing.weight,Drawing.more])

  parts = Part.select().where(Part.assembly == col)
  all = []
  for part in parts:
    oper = {'hole': 0, 'chamfer': 0, 'cgm': 0, 'saw': 0, 'milling': 0, 'notch': 0, 'bevel': 0}
    if part.chamfers.count() > 0:
      oper['chamfer'] = 1
    if part.holes.count() > 0:
      oper['hole'] = 1
    if part.profile == 'Лист':
      oper['cgm'] = 1
    else:
      oper['saw'] = 1
    if part.manipulation.find('фрез') >= 0:
      oper['milling'] = 1
    if part.manipulation.find('вырез') >= 0:
      oper['notch'] = 1
    if part.manipulation.find('скос') >= 0:
      oper['bevel'] = 1
    d = (point,part,detail,oper['hole'],oper['chamfer'],oper['cgm'],oper['saw'],oper['milling'],oper['notch'],oper['bevel'])
    all.append(d)
  with connection.atomic():
    PointPart.insert_many(all, fields=[PointPart.point,PointPart.part,PointPart.detail,PointPart.hole,PointPart.chamfer,PointPart.cgm,PointPart.saw,PointPart.milling,PointPart.notch,PointPart.bevel]).execute()
  