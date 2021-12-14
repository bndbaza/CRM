import csv
from os import replace
from db import connection
import datetime
from models import Drawing, Order, Point, Part, Weld, Bolt, Nut, Washer, Hole, Chamfer
Y = ('А','Б','В','Г','Д','Е','Ж','З','И','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х','Ц','Ч','Ш','Щ','Ы','Э','Ю','Я')

def Tekla(xls,yyy):
  yyy = Order.get_or_create(cas=yyy)
  parts = []
  dates = datetime.datetime.today()
  post = {'Drawing': [],'Point':[],'Part':[],'Weld':[],'Bolt':[],'Nut':[],'Washer':[],'Hole':[],'Chamfer':[],'Weight':[]}
  drawings = []
  non_drawing = Drawing.filter(cas=yyy[0])
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[0].replace(' ','') == 'DRAWING' and row[3].replace(' ','') == '1':
        non = False
        for i in non_drawing:
          if i.assembly == row[1].replace(' ',''):
            non = True
            break
        if non == True:
          non = False
          continue
        d = (row[1].replace(' ',''),float(row[4].replace(' ','')),yyy[0],dates,int(row[5].replace(' ','')))
        post['Drawing'].append(d)
  with connection.atomic():
    Drawing.insert_many(post['Drawing'], fields=[Drawing.assembly,Drawing.area,Drawing.cas,Drawing.create_date,Drawing.count]).execute()
    drawings = Drawing.filter(cas=yyy[0])
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      non = False
      for i in non_drawing:
        if i.assembly == row[1].replace(' ',''):
          non = True
          break
      if non == True:
        non = False
        continue
      if row[0].replace(' ','') == 'ASSEMBLY':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,
              row[3].replace(' ','').split('/')[0].split('-')[0],
              row[3].replace(' ','').replace('<','').replace('>','').split('/')[-1].split('-')[0],
              float(row[2].replace(' ','')),
              dates)
            post['Point'].append(d)
      if row[0].replace(' ','') == 'WELD':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,float(row[2].replace(' ','')),float(row[3].replace(' ','')),int(row[4].replace(' ','')),dates)
            post['Weld'].append(d)
      if row[0].replace(' ','') == 'BOLT':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[2].replace(' ',''),row[3].replace(' ',''),int(row[4].replace(' ','')),float(row[5].replace(' ','')),dates)
            post['Bolt'].append(d)
      if row[0].replace(' ','') == 'NUT':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[2].replace(' ',''),row[3].replace(' ',''),int(row[4].replace(' ','')),float(row[5].replace(' ','')),dates)
            post['Nut'].append(d)
      if row[0].replace(' ','') == 'WASHER':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[2].replace(' ',''),row[3].replace(' ',''),int(row[4].replace(' ','')),float(row[5].replace(' ','')),dates)
            post['Washer'].append(d)
      if row[0].replace(' ','') == 'PART':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,int(row[2].replace(' ','')),int(row[3].replace(' ','')),row[4].replace(' ',''),float(row[5].replace(' ','')),float(row[6].replace(' ','')),row[8].replace(' ',''),row[9].replace(' ',''),dates)
            post['Part'].append(d)
  with connection.atomic():
    Part.insert_many(post['Part'], fields=[Part.assembly,Part.number,Part.count,Part.profile,Part.length,Part.weight,Part.mark,Part.manipulation,Part.create_date]).execute()
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      non = False
      for i in non_drawing:
        if i.assembly == row[1].replace(' ',''):
          non = True
          break
      if non == True:
        non = False
        continue
      if row[0].replace(' ','') == 'HOLE':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            part = Part.get(number=int(row[2].replace(' ','')),assembly=col)
            d = (part,int(row[3].replace(' ','')),int(row[4].replace(' ','')),int(row[5].replace(' ','')) / 2,dates)
            post['Hole'].append(d)
      if row[0].replace(' ','') == 'CHAMFER':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            part = Part.get(number=int(row[2].replace(' ','')),assembly=col)
            d = (part,float(row[3].replace(' ','')),dates)
            post['Chamfer'].append(d)
  with connection.atomic():
    Point.insert_many(post['Point'], fields=[Point.assembly,Point.point_x,Point.point_y,Point.point_z,Point.create_date]).execute()
    Weld.insert_many(post['Weld'], fields=[Weld.assembly,Weld.cathet,Weld.length,Weld.count,Weld.create_date]).execute()
    Bolt.insert_many(post['Bolt'], fields=[Bolt.assembly,Bolt.profile,Bolt.gost,Bolt.count,Bolt.weight,Bolt.create_date]).execute()
    Nut.insert_many(post['Nut'], fields=[Nut.assembly,Nut.profile,Nut.gost,Nut.count,Nut.weight,Nut.create_date]).execute()
    Washer.insert_many(post['Washer'], fields=[Washer.assembly,Washer.profile,Washer.gost,Washer.count,Washer.weight,Washer.create_date]).execute()
    Hole.insert_many(post['Hole'], fields=[Hole.part,Hole.diameter,Hole.count,Hole.depth,Hole.create_date]).execute()
    Chamfer.insert_many(post['Chamfer'], fields=[Chamfer.part,Chamfer.length,Chamfer.create_date]).execute()


  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row[0].replace(' ','') == 'WEIGHT':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            if row[3].replace(' ','') != '':
              more = 0
              more = float(row[3].replace(' ','').split(';')[1])  / col.count
            else:
              more = 0
            col.weight = float(row[2].replace(' ','')) / col.count,
            col.more=more,
            post['Weight'].append(col)
  with connection.atomic():
    Drawing.bulk_update(post['Weight'], fields=[Drawing.weight,Drawing.more])
  return
      
