import csv
from datetime import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.styles.numbers import BUILTIN_FORMATS
from models import *
from peewee import fn
from tekla import Size,Test
from db import connection

def Replace():
  before = 'МБ2-325'
  after = 'МБ2-56'
  pp_b = PointPart.select().join(Point).join(Drawing).where(Drawing.assembly == before)
  detail = pp_b[0].detail
  point = pp_b[0].point
  pp_a = PointPart.select().join(Point).join(Drawing).where(Drawing.assembly == after).group_by(PointPart.part)
  point.assembly = pp_a[0].point.assembly
  point.draw = pp_a[0].point.draw
  point.save()
  ppp = Part.select(Part.id).join(Drawing).where(Drawing.assembly == before).tuples()
  print(ppp[0])
  for p in pp_a:
    PointPart.create(
      point=point,
      part=p.part,
      detail=detail,
      cgm=p.cgm,
      saw=p.saw,
      hole=p.hole,
      bevel=p.bevel,
      notch=p.notch,
      chamfer=p.chamfer,
      milling=p.milling,
      bend=p.bend,
      weld=p.weld,
      turning=p.turning,
      joint=p.joint
    )
  return
  TaskPart.delete().where(TaskPart.part.in_(ppp)).execute()
  Hole.delete().where(Hole.part.in_(ppp)).execute()
  Chamfer.delete().where(Chamfer.part.in_(ppp)).execute()
  PointPart.delete().where(PointPart.part.in_(ppp)).execute()
  Part.delete().where(Part.id.in_(ppp)).execute()
  dr = Drawing.get(Drawing.assembly == before)
  Bolt.delete().where(Bolt.assembly == dr).execute()
  Nut.delete().where(Nut.assembly == dr).execute()
  Washer.delete().where(Washer.assembly == dr).execute()
  Weld.delete().where(Weld.assembly == dr).execute()
  Drawing.delete().where(Drawing.assembly == before).execute()

  # point = Point.select().join(Drawing).where()
  # for

def Correction(mark,order):
  er = mark
  drawing = {'DRAWING':[],'ASSEMBLY':[],'PART':[],'WEIGHT':[],'WELD':[],'BOLT':[],'NUT':[],'WASHER':[],'HOLE':[],'CHAMFER':[]}
  post = {'Drawing': [],'Point':[],'Part':[],'Weld':[],'Bolt':[],'Nut':[],'Washer':[],'Hole':[],'Chamfer':[],'Weight':[]}
  with open('23253.xls','r', encoding='windows-1251',newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[1].replace(' ','') == er:
        d = []
        for i in row:
          d.append(i.replace(' ',''))
        drawing[row[0].replace(' ','')].append(d)
  pp = PointPart.select().join(Point).join(Drawing).join(Order).where(Drawing.assembly == er,Drawing.cas == order)
  point = pp[0].point
  detail = pp[0].detail
  col = Drawing.get(Drawing.assembly == er,Drawing.cas == order)
  col.area = float(drawing['DRAWING'][0][4])
  col.count = int(drawing['DRAWING'][0][5])
  col.weight = float(drawing['WEIGHT'][0][2])
  if drawing['WEIGHT'][0][3] != '':
    col.more = float(drawing['WEIGHT'][0][3].split(';')[1])
  else:
    col.more = float(0)
  col.save()
  ass = Point.select().join(Drawing).where(Drawing.assembly == er,Drawing.cas == order,
                                            Point.point_x == drawing['ASSEMBLY'][0][3].split('/')[0],
                                            Point.point_y == drawing['ASSEMBLY'][0][3].split('/')[1],
                                            Point.point_z == float(drawing['ASSEMBLY'][0][2])).first()
  parts = Part.select().join(Drawing).where(Drawing.assembly == er,Drawing.cas == order)
  pr = []
  for cor in drawing['PART']:
    err = 2
    for i in parts:
      if i.number == int(cor[2]):
        err = 1
        if i.weight != float(cor[6]):
          i.weight = float(cor[6])
          i.save()
        if i.length != int(cor[5]):
          i.length = int(cor[5])
          i.save()
        if float(i.area) != float(cor[13]):
          i.area = float(cor[13])
          print(cor)
          i.save()
        if i.mark != cor[8]:
          i.mark = cor[8]
          i.save()
        if i.manipulation != cor[9]:
          i.manipulation = cor[9]
          i.save()
        if i.count == int(cor[3]):
          err = 0
        else:
          print(i)
          i.count = int(cor[3])
          i.save()
    if err == 2:
      correct = {'Hole':[],'Chamfer':[]}
      # print(drawing['HOLE'])
      i = cor
      profile = Size(i[4])
      part = Part.create(assembly=col,
                            number=int(i[2]),
                            count=int(i[3]),
                            profile=profile[0],
                            size=profile[1],
                            length=float(i[5]),
                            weight=float(i[6]),
                            mark=i[8],
                            manipulation=i[9],
                            work=profile[2],
                            width=profile[3],
                            perimeter=int(Test(i[11])),
                            depth=float(Test(i[12],profile[1])),
                            create_date=datetime.datetime.today())
      for i in drawing['HOLE']:
        # part = Part.get(number=int(i[2]),assembly=col)
        if part.profile == 'Лист' and int(part.size) < 14:
          pass
        else:
          correct['Hole'].append((part,int(i[3]),(int(i[4]))/part.count,int(i[5]) / 2,datetime.datetime.today()))
      for i in drawing['CHAMFER']:
        # part = Part.get(number=int(i[2]),assembly=col)
        if part.number == int(i[2]):
          correct['Chamfer'].append((part,float(i[3]),datetime.datetime.today()))
      with connection.atomic():
        Hole.insert_many(correct['Hole'], fields=[Hole.part,Hole.diameter,Hole.count,Hole.depth,Hole.create_date]).execute()
        Chamfer.insert_many(correct['Chamfer'], fields=[Chamfer.part,Chamfer.length,Chamfer.create_date]).execute()
      oper = {'hole': 0, 'chamfer': 0, 'cgm': 0, 'saw': 0, 'milling': 0, 'notch': 0, 'bevel': 0, 'joint':0,'bend':0,'turning':0}
      if part.chamfers.count() > 0:
        oper['chamfer'] = 1
      if part.holes.count() > 0:
        oper['hole'] = 1
      if part.profile == 'Лист':
        oper['cgm'] = 1
      elif part.profile == 'Паронит' or part.profile == 'Резина' or part.profile == 'Стекло':
        pass
      else:
        oper['saw'] = 1
      if part.manipulation.find('фрез') >= 0:
        oper['milling'] = 1
      if part.manipulation.find('вырез') >= 0:
        oper['notch'] = 1
      if part.manipulation.find('скос') >= 0:
        oper['bevel'] = 1
      if part.manipulation.find('стык') >= 0:
        oper['joint'] = 1
      if part.manipulation.find('гиб') >= 0:
        oper['bend'] = 1
      if part.manipulation.find('ток') >= 0:
        oper['turning'] = 1
      if part.manipulation.find('резьба') >= 0:
        oper['turning'] = 1
      PointPart.create(point=point,
                        part=part,
                        detail=detail,
                        hole=oper['hole'],
                        chamfer=oper['chamfer'],
                        cgm=oper['cgm'],
                        saw=oper['saw'],
                        milling=oper['milling'],
                        notch=oper['notch'],
                        bevel=oper['bevel'],
                        joint=oper['joint'],
                        bend=oper['bend'],
                        turning=oper['turning'])
  # if len(parts) > len(drawing['PART']):
  for p in parts:
    ok = False
    for d in drawing['PART']:
      if p.number == int(d[2]):
        ok = True
    if ok == False:
      p.delete_instance(recursive=True)

  # print(drawing['PART'])

  return
  PointPart.delete().where(PointPart.detail == detail).execute()
  Weld.delete().where(Weld.assembly == col).execute()
  Bolt.delete().where(Bolt.assembly == col).execute()
  Nut.delete().where(Nut.assembly == col).execute()
  Washer.delete().where(Washer.assembly == col).execute()
  part_d = Part.select(Part.id).where(Part.assembly == col).tuples()
  Hole.delete().where(Hole.part.in_(part_d)).execute()
  Chamfer.delete().where(Chamfer.part.in_(part_d)).execute()
  Part.delete().where(Part.assembly == col).execute()
  dates = datetime.datetime.today()
  print(point,detail,col,dates)
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
    oper = {'hole': 0, 'chamfer': 0, 'cgm': 0, 'saw': 0, 'milling': 0, 'notch': 0, 'bevel': 0, 'joint':0,'bend':0,'turning':0}
    if part.chamfers.count() > 0:
      oper['chamfer'] = 1
    if part.holes.count() > 0:
      oper['hole'] = 1
    if part.profile == 'Лист':
      oper['cgm'] = 1
    elif part.profile == 'Паронит' or part.profile == 'Резина' or part.profile == 'Стекло':
      pass
    else:
      oper['saw'] = 1
    if part.manipulation.find('фрез') >= 0:
      oper['milling'] = 1
    if part.manipulation.find('вырез') >= 0:
      oper['notch'] = 1
    if part.manipulation.find('скос') >= 0:
      oper['bevel'] = 1
    if part.manipulation.find('стык') >= 0:
      oper['joint'] = 1
    if part.manipulation.find('гиб') >= 0:
      oper['bend'] = 1
    if part.manipulation.find('ток') >= 0:
      oper['turning'] = 1
    if part.manipulation.find('резьба') >= 0:
      oper['turning'] = 1
    d = (point,part,detail,oper['hole'],oper['chamfer'],oper['cgm'],oper['saw'],oper['milling'],oper['notch'],oper['bevel'],oper['joint'],oper['bend'],oper['turning'])
    all.append(d)
  with connection.atomic():
    PointPart.insert_many(all, fields=[PointPart.point,PointPart.part,PointPart.detail,PointPart.hole,PointPart.chamfer,PointPart.cgm,PointPart.saw,PointPart.milling,PointPart.notch,PointPart.bevel,PointPart.joint,PointPart.bend,PointPart.turning]).execute()

def PointCorrect(mark,t,s):
  try:
    point = Point.select().join(Drawing).where(Point.point_x == s[0]['point_x'],Point.point_y == s[0]['point_y'],Point.point_z == s[0]['point_z'],Point.draw == s[0]['draw'],Point.name == s[0]['name'],Drawing.assembly == mark).first()
    point_x = (t[0]['point_x']),
    point.point_x = point_x[0],
    point_y = (t[0]['point_y']),
    point.point_y = point_y[0],
    point_z = (t[0]['point_z']),
    point.point_z = point_z[0],
    draw = (t[0]['draw']),
    draw = draw[0]
    point.draw = draw,
    name = (t[0]['name']),
    point.name = name[0]
    point.save()
    points = Point.select().where(Point.id == point.id)
    print(type(point.point_x))
    print(point.point_x)
    for point in points:
      point.draw = point.draw.replace('(','').replace("'",'').replace(')','').replace(',','')
      point.point_x = point.point_x.replace('(','').replace("'",'').replace(')','').replace(',','')
      point.point_y = point.point_y.replace('(','').replace("'",'').replace(')','').replace(',','')
      print(point.draw)
      point.save()
  except:
    print(mark,t,s)
