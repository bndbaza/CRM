from db import connection
from models import *
from datetime import datetime

def TeklaAdd(add,tekla,case):
  case = Order.get_or_create(cas=case)[0]
  date = datetime.today()
  post = {'Drawing': [],'Point':[],'Part':[],'Weld':[],'Bolt':[],'Nut':[],'Washer':[],'Hole':[],'Chamfer':[],'Weight':[]}
  for ad in add:
    drawing = Drawing.get(Drawing.assembly == ad)
    drawing.count = add[ad]['count']
    drawing.save()
    for assembly in add[ad]['assembly']:
      post['Point'].append((drawing,assembly['point_x'],assembly['point_y'],assembly['point_z'],assembly['name'],assembly['draw'],date))


  for i in tekla:
    drawing = Drawing.create(assembly=i,area=tekla[i]['area'],cas=case,create_date=date,count=tekla[i]['count'],weight=tekla[i]['weight']['weight'],more=tekla[i]['weight']['more'])
    for assembly in tekla[i]['point']:
      post['Point'].append((drawing,assembly['point_x'],assembly['point_y'],assembly['point_z'],assembly['name'],assembly['draw'],date))
    for weld in tekla[i]['weld']:
      post['Weld'].append((drawing,weld['cathet'],weld['length'],weld['count'],date))
    for bolt in tekla[i]['bolt']:
      post['Bolt'].append((drawing,bolt['profile'],bolt['gost'],bolt['count'],bolt['weight'],date))
    for nut in tekla[i]['nut']:
      post['Nut'].append((drawing,nut['profile'],nut['gost'],nut['count'],nut['weight'],date))
    for washer in tekla[i]['washer']:
      post['Washer'].append((drawing,washer['profile'],washer['gost'],washer['count'],washer['weight'],date))
    for p in tekla[i]['part']:
      part = Part.create(
        assembly=drawing,
        number=p,
        count=tekla[i]['part'][p]['count'],
        profile=tekla[i]['part'][p]['profile'],
        size=tekla[i]['part'][p]['size'],
        length=tekla[i]['part'][p]['length'],
        weight=tekla[i]['part'][p]['weight'],
        mark=tekla[i]['part'][p]['mark'],
        manipulation=tekla[i]['part'][p]['manipulation'],
        work=tekla[i]['part'][p]['work'],
        width=tekla[i]['part'][p]['width'],
        perimeter=tekla[i]['part'][p]['perimeter'],
        depth=tekla[i]['part'][p]['depth'],
        area=tekla[i]['part'][p]['area'],
        create_date=date
      )
      for hole in tekla[i]['part'][p]['hole']:
        post['Hole'].append((part,hole['diameter'],hole['count'],hole['depth'],date))
      if tekla[i]['part'][p]['chamfer'] != {}:
        post['Chamfer'].append((part,tekla[i]['part'][p]['chamfer']['length'],date))
      

  with connection.atomic():
    Point.insert_many(post['Point'], fields=[Point.assembly,Point.point_x,Point.point_y,Point.point_z,Point.name,Point.draw,Point.create_date]).execute()
    Weld.insert_many(post['Weld'], fields=[Weld.assembly,Weld.cathet,Weld.length,Weld.count,Weld.create_date]).execute()
    Bolt.insert_many(post['Bolt'], fields=[Bolt.assembly,Bolt.profile,Bolt.gost,Bolt.count,Bolt.weight,Bolt.create_date]).execute()
    Nut.insert_many(post['Nut'], fields=[Nut.assembly,Nut.profile,Nut.gost,Nut.count,Nut.weight,Nut.create_date]).execute()
    Washer.insert_many(post['Washer'], fields=[Washer.assembly,Washer.profile,Washer.gost,Washer.count,Washer.weight,Washer.create_date]).execute()
    Hole.insert_many(post['Hole'], fields=[Hole.part,Hole.diameter,Hole.count,Hole.depth,Hole.create_date]).execute()
    Chamfer.insert_many(post['Chamfer'], fields=[Chamfer.part,Chamfer.length,Chamfer.create_date]).execute()
  