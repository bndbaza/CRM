import csv
from os import replace
from db import connection
import datetime
from models import Drawing, Order, Point, Part, Weld, Bolt, Nut, Washer, Hole, Chamfer
clr = (('green','white'),('blue','white'),('yellow','black'),('red','white'),('grey','black'),('black','white'),('pink','black'))

def Tekla(xls,yyy):
  yyy = Order.get_or_create(cas=yyy)
  parts = []
  dates = datetime.datetime.today()
  post = {'Drawing': [],'Point':[],'Part':[],'Weld':[],'Bolt':[],'Nut':[],'Washer':[],'Hole':[],'Chamfer':[],'Weight':[]}
  drawings = []
  with open(xls.filename,'r', encoding='windows-1251',newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row == []: continue
      if row[0].replace(' ','') == 'DRAWING' and row[3].replace(' ','') == '1' and row[1].replace(' ','').find('(?)') == -1:
        d = (row[1].replace(' ',''),float(row[4].replace(' ','')),yyy[0],dates,int(row[5].replace(' ','')))
        try:
          res = Drawing.get(Drawing.assembly == row[1].replace(' ',''),Drawing.cas == yyy[0])
          res.count = int(row[5].replace(' ',''))
          res.create_date = dates
          res.area = float(row[4].replace(' ',''))
          res.save()
        except:
          post['Drawing'].append(d)
  with connection.atomic():
    Drawing.insert_many(post['Drawing'], fields=[Drawing.assembly,Drawing.area,Drawing.cas,Drawing.create_date,Drawing.count]).execute()
    drawings = Drawing.filter(cas=yyy[0])
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row == []: continue
      if row[0].replace(' ','') == 'ASSEMBLY':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            try:
              if row[7].replace(' ','') == '':
                draw = None
              else:
                draw = int(row[7].replace(' ',''))
            except:
              draw = None
            d = (col,
              row[3].replace(' ','').replace('<','').replace('>','').split('/')[0].split('-')[0],
              row[3].replace(' ','').replace('<','').replace('>','').split('/')[-1].split('-')[0],
              float(row[2].replace(' ','')),
              row[5].strip(),
              draw,
              dates)
            try:
              Point.get(Point.assembly == col,
                        Point.point_x == row[3].replace(' ','').replace('<','').replace('>','').split('/')[0].split('-')[0],
                        Point.point_y == row[3].replace(' ','').replace('<','').replace('>','').split('/')[-1].split('-')[0],
                        Point.point_z == float(row[2].replace(' ','')),
                        Point.name == row[5].strip(),
                        Point.draw == draw)
            except:
              post['Point'].append(d)
      if row[0].replace(' ','') == 'WELD':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,float(row[2].replace(' ','')),float(row[3].replace(' ','')),int(row[4].replace(' ','')),dates)
            try:
              Weld.get(Weld.assembly == col,Weld.cathet == float(row[2].replace(' ','')),Weld.length == float(row[3].replace(' ','')),Weld.count == int(row[4].replace(' ','')))
            except:
              post['Weld'].append(d)
      if row[0].replace(' ','') == 'BOLT':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[2].replace(' ',''),row[3].replace(' ',''),int(row[4].replace(' ','')),float(row[5].replace(' ','')),dates)
            try:
              Bolt.get(Bolt.assembly == col,Bolt.profile == row[2].replace(' ',''),Bolt.gost == row[3].replace(' ',''),Bolt.count == int(row[4].replace(' ','')),Bolt.weight == float(row[5].replace(' ','')))
            except:
              post['Bolt'].append(d)
      if row[0].replace(' ','') == 'NUT':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[2].replace(' ',''),row[3].replace(' ',''),int(row[4].replace(' ','')),float(row[5].replace(' ','')),dates)
            try:
              Nut.get(Nut.assembly == d[0],Nut.profile == d[1],Nut.gost == d[2],Nut.count == d[3],Nut.weight == d[4])
            except:
              post['Nut'].append(d)
      if row[0].replace(' ','') == 'WASHER':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            d = (col,row[2].replace(' ',''),row[3].replace(' ',''),int(row[4].replace(' ','')),float(row[5].replace(' ','')),dates)
            try:
              Washer.get(Washer.assembly == d[0],Washer.profile == d[1],Washer.gost == d[2],Washer.count == d[3],Washer.weight == d[4])
            except:
              post['Washer'].append(d)
      if row[0].replace(' ','') == 'PART':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            profile = Size(row[4].replace(' ',''))
            d = (col,
                int(row[2].replace(' ','')),
                int(row[3].replace(' ','')),
                profile[0],
                profile[1],
                float(row[5].replace(' ','')),
                float(row[6].replace(' ','')),
                row[8].replace(' ',''),
                row[9].replace(' ',''),
                profile[2],
                profile[3],
                int(Test(row[11].replace(' ',''))),
                float(Test(row[12].replace(' ',''),profile[1])),
                dates)
            try:
              Part.get(Part.assembly == d[0],
                      Part.number == d[1],
                      Part.count == d[2],
                      Part.profile == d[3],
                      Part.size == d[4],
                      Part.length == d[5],
                      Part.weight == d[6],
                      Part.mark == d[7],
                      Part.manipulation == d[8],
                      Part.work == d[9],
                      Part.width == d[10],
                      Part.perimeter == d[11],
                      Part.depth == d[12])
            except:
              post['Part'].append(d)
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
  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row == []: continue
      if row[0].replace(' ','') == 'HOLE':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            part = Part.get(number=int(row[2].replace(' ','')),assembly=col)
            if part.profile == 'Лист' and int(part.size) < 15:
              pass
            else:
              d = (part,int(row[3].replace(' ','')),(int(row[4].replace(' ','')))/part.count,int(row[5].replace(' ','')) / 2,dates)
              try:
                Hole.get(Hole.part == d[0],Hole.diameter == d[1],Hole.count == d[2],Hole.depth == d[3])
              except:
                post['Hole'].append(d)
      if row[0].replace(' ','') == 'CHAMFER':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            part = Part.get(number=int(row[2].replace(' ','')),assembly=col)
            d = (part,float(row[3].replace(' ','')),dates)
            post['Chamfer'].append(d)
  with connection.atomic():
    Point.insert_many(post['Point'], fields=[Point.assembly,Point.point_x,Point.point_y,Point.point_z,Point.name,Point.draw,Point.create_date]).execute()
    Weld.insert_many(post['Weld'], fields=[Weld.assembly,Weld.cathet,Weld.length,Weld.count,Weld.create_date]).execute()
    Bolt.insert_many(post['Bolt'], fields=[Bolt.assembly,Bolt.profile,Bolt.gost,Bolt.count,Bolt.weight,Bolt.create_date]).execute()
    Nut.insert_many(post['Nut'], fields=[Nut.assembly,Nut.profile,Nut.gost,Nut.count,Nut.weight,Nut.create_date]).execute()
    Washer.insert_many(post['Washer'], fields=[Washer.assembly,Washer.profile,Washer.gost,Washer.count,Washer.weight,Washer.create_date]).execute()
    Hole.insert_many(post['Hole'], fields=[Hole.part,Hole.diameter,Hole.count,Hole.depth,Hole.create_date]).execute()
    Chamfer.insert_many(post['Chamfer'], fields=[Chamfer.part,Chamfer.length,Chamfer.create_date]).execute()


  with open(xls.filename,'r', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
      if row == []: continue
      if row[0].replace(' ','') == 'WEIGHT':
        for col in drawings:
          if row[1].replace(' ','') == col.assembly:
            if row[3].replace(' ','') != '':
              more = 0
              more = float(row[3].replace(' ','').split(';')[1])
            else:
              more = 0
            col.weight = float(row[2].replace(' ','')),
            col.more=more,
            post['Weight'].append(col)
  with connection.atomic():
    Drawing.bulk_update(post['Weight'], fields=[Drawing.weight,Drawing.more])
  return

def Size(str):
  if str == 'TK52х4':
    print(str)
  str = str.replace('x','х')
  if str.startswith('Гн.[]'):
    if int(str.replace('Гн.[]','').split('х')[0]) >= 160:
      i = ('Труба профильная',str.replace('Гн.[]',''),'saw_b','')
    else:
      i = ('Труба профильная',str.replace('Гн.[]',''),'saw_s','')
    return (i)
  elif str.startswith('Гн.['):
    if int(str.replace('Гн.[','').split('х')[0]) >= 200:  
      i = ('Швеллер гнутый',str.replace('Гн.[',''),'saw_b','')
    else:
      i = ('Швеллер гнутый',str.replace('Гн.[',''),'saw_s','')
    return (i)
  elif str.startswith('Гн.'):  
    if int(str.replace('Гн.','').split('х')[0]) >= 160: 
      i = ('Труба профильная',str.replace('Гн.',''),'saw_b','')
    else:
      i = ('Труба профильная',str.replace('Гн.',''),'saw_s','')
    return (i)

  elif str.startswith('ПК'):  
    if int(str.replace('ПК','').split('х')[0]) >= 160: 
      i = ('Труба профильная',str.replace('ПК',''),'saw_b','')
    else:
      i = ('Труба профильная',str.replace('ПК',''),'saw_s','')
    return (i)

  elif str.startswith('['):
    if int(str.replace('[','').replace('П','').replace('У','')) >= 20:
      i = ('Швеллер',str.replace('[',''),'saw_b','')
    else:
      i = ('Швеллер',str.replace('[',''),'saw_s','')
    return (i)
  elif str.startswith('O'):
    i = ('Круг',str.replace('O',''),'saw_s','')
    return (i)

  elif str.startswith('ТК'):
    if float(str.replace('ТК','').split('х')[0]) >= 273:
      i = ('Труба круглая',str.replace('ТК',''),'saw_b','')
    else:
      i = ('Труба круглая',str.replace('ТК',''),'saw_s','')

    return (i)
  elif str.startswith('TЭ'):
    if float(str.replace('TЭ','').split('х')[0]) >= 273:
      i = ('Труба круглая',str.replace('TЭ',''),'saw_b','')
    else:
      i = ('Труба круглая',str.replace('TЭ',''),'saw_s','')
    return (i)
  elif str.startswith('TБ'):
    if float(str.replace('TБ','').split('х')[0]) >= 273:
      i = ('Труба круглая',str.replace('TБ',''),'saw_b','')
    else:
      i = ('Труба круглая',str.replace('TБ',''),'saw_s','')
    return (i)
  elif str.startswith('L'):
    if int(str.replace('L','').split('х')[0]) >= 200:
      i = ('Уголок',str.replace('L',''),'saw_b','')
    else:
      i = ('Уголок',str.replace('L',''),'saw_s','')
    return (i)
  elif str.startswith('I'):  
    i = ('Двутавр',str.replace('I',''),'saw_b','')
    return (i)
  elif str.startswith('—'):
    a = str.replace('—','').split('х')
    if int(a[0]) > int(a[1]):
      i = ('Лист',a[1],'cgm',a[0])
    else:
      i = ('Лист',a[0],'cgm',a[1])
    return (i)
  elif str.startswith('-'):  
    a = str.replace('-','').split('х')
    if int(a[0]) > int(a[1]):
      i = ('Лист',a[1],'cgm',a[0])
    else:
      i = ('Лист',a[0],'cgm',a[1])
    return (i)
  elif str.startswith('Риф'):  
    a = str.replace('Риф','').split('х')
    if int(a[0]) > int(a[1]):
      i = ('Лист РИФ',a[1],'cgm',a[0])
    else:
      i = ('Лист РИФ',a[0],'cgm',a[1])
    return (i)
  elif str.startswith('ПВ'):  
    a = str.replace('ПВ','').split('х')
    if int(a[0]) > int(a[1]):
      i = ('Лист ПВ',a[1],'cgm',a[0])
    else:
      i = ('Лист ПВ',a[0],'cgm',a[1])
    return (i)
  elif str.startswith('TK'):
    if float(str.replace('TK','').split('х')[0]) >= 273:
      i = ('Труба круглая',str.replace('TK',''),'saw_b','')
    else:
      i = ('Труба круглая',str.replace('TK',''),'saw_s','')
    return (i)

def Test(i,size=0):
  if i == '' and size != 0:
    size = size.split('х')
    return size[-1]
  elif i == '' and size == 0:
    return 0
  else:
    return i