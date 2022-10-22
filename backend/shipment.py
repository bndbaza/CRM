import asyncio
from send_bot import Bots
from models import *
from db import server_host,connection
from peewee import fn, JOIN, Case


async def Get(msgs):
  connection.close()
  msg = msgs.split(' ')
  if msg[0] == 'Run':
    if Shipment.select().where(Shipment.date == None).first() != None:
      await Ship(msg)
      return
    detail = Faza.select().where(Faza.detail == msg[1]).first()
    if detail == None:
      await Bots(f'{msg[1]} Наряд не существует')
      return
    if detail.packed == 0:
      await Bots(f'{msg[1]} Наряд не сдан в отгрузку')
      if detail.paint == 1:
        # Detail.update({
        #   Detail.start: datetime.datetime.today(),
        #   Detail.end: datetime.datetime.today(),
        #   Detail.worker_1: 92,
        # }).where(Detail.detail == msg[1],Detail.oper == 'paint').execute()
        # detail.paint = 3
        # detail.packed = 1
        # detail.save()
        await Bots(f'{msg[1]} Наряд не окрашивался!!!')
        return
      elif detail.paint == 3:
        # Otc.update({Otc.worker: 139,Otc.end: datetime.datetime.today()}).where(Otc.detail == detail).execute()
        # detail.packed = 1
        # detail.save()
        await Bots(f'{msg[1]} Наряд не принят ОТК!!!')
        return
      elif detail.paint == 2:
        # Detail.update({
        #   Detail.end: datetime.datetime.today(),
        # }).where(Detail.detail == msg[1],Detail.oper == 'paint').execute()
        # detail.paint = 3
        # detail.packed = 1
        # detail.save()
        await Bots(f'{msg[1]} Окрашивание не закончено!!!')
        return
      else:
        await Bots(f'{msg[1]} ПОТЕРЯЛСЯ')
        return
    pack = DetailPack.get_or_create(detail=detail)
    if pack[1] == True:
      pp = PointPart.select(PointPart,fn.COUNT(Part.id).alias('count')).join(Part).join(Drawing).where(Drawing.cas == 15,PointPart.weld == 0,PointPart.detail == msg[1],PointPart.detail < 2493).group_by(PointPart.detail,Part.id)
      if len(pp) != 0:
        await Bots(f'Наряд может иметь более одной позиции, сверьтесь со списком')
    else:
      try:
        await Bots(f'Пачка {pack[0].pack.number}')
      except:
        print(pack)

  elif msgs == 'PACKAGE':
    details = DetailPack.select().where(DetailPack.pack == None)
    if len(details) != 0:
      order = details[0].detail.case
      number = Packed.select(fn.MAX(Packed.number)).scalar()
      if number == None:
        number = 0
      pack = Packed.create(number=number + 1,order=order)
      for detail in details:
        detail.pack = pack
      with connection.atomic():
        DetailPack.bulk_update(details,fields=[DetailPack.pack])
      package = DetailPack.select(fn.SUM(Faza.weight).alias('weight')).join(Faza).where(DetailPack.pack == pack).group_by(DetailPack.pack).scalar()
      text = ''
      text += f'Пачка: {pack.number} Вес: {package}\n'
      for d in details:
        text += f'Наряд {d.detail.detail}\n'
      await Bots(text)
  
  elif msgs == 'CLEAR':
    DetailPack.delete().where(DetailPack.pack == None).execute()
  
  elif msg[0] == 'P':
    ship = Shipment.select().where(Shipment.date == None).first()
    if ship == None:
      await Bots('Нет машины для погрузки')
    else:
      pack = Packed.select().where(Packed.number == msg[1]).first()
      pack.shipment = ship
      pack.save()
      weight = Shipment.select(fn.SUM(Faza.weight)).join(Packed).join(DetailPack).join(Faza).where(Shipment.id == pack.shipment).scalar()
      await Bots(f'Пачка {pack.number} заргужена в машину. В машине {weight} кг.')


  

async def handle_client(reader, writer):
  print(f'Connect')
  request = None
  while request != '':
    request = (await reader.read(255)).decode('utf8')
    msg = request.replace('\r','').replace('\n','')
    if request != '':
      await Get(msg)
    else:
      print('Disconnect')
  writer.close()

async def Start():
  server = await asyncio.start_server(handle_client, server_host, 2000)
  async with server:
    await server.serve_forever()

async def Ship(msg):
  ship = Shipment.select().where(Shipment.date == None).first()
  pack = Packed.select().join(DetailPack).join(Faza).where(Faza.detail == msg[1]).first()
  if pack == None:
    await Bots(f'Наряд {msg[1]} не собран в пачку')
  else:
    pack.shipment = ship
    pack.save()
    weight = Shipment.select(fn.SUM(Faza.weight)).join(Packed).join(DetailPack).join(Faza).where(Shipment.id == pack.shipment).scalar()
    await Bots(f'Пачка {pack.number} заргужена в машину. В машине {weight} кг.')

