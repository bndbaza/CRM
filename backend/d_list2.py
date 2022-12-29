from models import *
from peewee import fn
from datetime import datetime
from tekla3 import PdfGenerate, PointPartInsert


def ManualUpload(marks):
    manipulations = {
        'bevel':'скос',
        'notch':'вырез',
        'chamfer':'фаска',
        'milling':'фрез',
        'bend':'гиб',
        'turning': 'ток'
      }
    case = Order.get(Order.cas == marks.case)
    marks = marks.marks
    index = 0
    faza = Faza.select(fn.MAX(Faza.faza)).where(Faza.case == case).scalar()
    date = datetime.today()
    if faza:
        faza += 1
    else:
        faza = 1
    for mark in marks:
        weight_mark = 0
        print(mark)
        paint = int(mark.paint)
        drawing = Drawing.create(create_date=date,cas=case,assembly=mark.mark,area=0,count=mark.count,weight=0,more=0,paint=paint)
        try:
            welds = mark.weld.split(',')
            for w in welds:
                cat = w.split('=')
                weld = Weld.create(create_date=date,assembly=drawing,cathet=int(cat[0]),length=float(cat[1]),count=0)
        except:
            pass
        for i in range(mark.count):
            point = Point.create(create_date=date,assembly=drawing,name=mark.name,point_x='0',point_y='0',point_z=0,in_work=0,draw=mark.draw,faza=faza)
        for detail in mark.details:
            catalog = CatalogSteel.get(CatalogSteel.id == detail.id)
            index += 1
            manipulation = ''
            
            for m in detail.manipulation:
                manipulation += manipulations[m]
                manipulation += ','

            if detail.width:
                width = str(detail.width)
                weight = float(detail.width/1000) * float(detail.lenght/1000) * float(catalog.weight)
                work = 'cgm'
            else:
                width = ''
                weight = float(detail.lenght/1000) * float(catalog.weight)
                work = 'saw_b'
            weight_mark += weight * detail.count
            part = Part.create(assembly=drawing,
                               number=detail.number,
                               count=detail.count,
                               size=catalog.size,
                               profile=catalog.name,
                               width=width,
                               length=detail.lenght,
                               mark=catalog.mark,
                               depth=0,
                               perimeter=0,
                               sn=detail.number,
                               area=0,
                               weight=weight,
                               manipulation=manipulation,
                               work=work,
                               create_date=date)
            try:
                holes = detail.hole.split(',')
                for h in holes:
                    hol = h.split('=')
                hole = Hole.create(create_date=date,part=part,diameter=hol[1],count=hol[0],depth=20)
            except:
                pass
        print(weight_mark)
        drawing.weight = weight_mark
        drawing.save()
    print((faza,),case.cas)
    PointPartInsert((faza,),case.cas)
    PdfGenerate((faza,),case.cas)
