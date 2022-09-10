from typing import Text
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from peewee import fn

from models import *
from db import bot_id
from bot_command import *
from send_bot import TechBirk

bot = Bot(bot_id)
dp = Dispatcher(bot)

# Команда start
@dp.message_handler(commands=['start'])
async def start(message):
  if User.select().where(User.telegram == message.from_user.id).first() != None:
    text = 'Вы зарегистрированы, можете приступать к работе'
  else:
    text = 'Для регистрации отправьте "Регистрация Фамилия Имя Отчество" и ожидайте подтверждения'
  await bot.send_message(message.from_user.id,text)
  connection.close()

# Регистрация
@dp.message_handler(lambda message: message.text.lower().startswith('регистрация '))
async def registration(message):
  text = message.text.split(' ')
  result = await Registration(message,text)
  await bot.send_message(message.from_user.id,result)
  await message.delete()
  connection.close()


# Проверка на регистрацию
@dp.message_handler(lambda message: User.select().where(User.telegram == message.from_user.id).first() == None)
async def no_registration(message):
  await bot.send_message(message.from_user.id,'Вы не зарегистрироранны')
  connection.close()

# Удаление пачек
@dp.message_handler(lambda message: Group(message,['admin','shipment']) and message.text.lower().startswith('d '))
async def delete_pack(message):
  pack = int(message.text.replace('d ','').replace('D ',''))
  if pack == 0:
    DetailPack.delete().where(DetailPack.pack == None).execute()
    await message.answer(f'Список очищен')
  else:
    p = Packed.select().where(Packed.number == pack).first()
    if p:
      detail = DetailPack.select(Faza.detail).join(Faza).where(DetailPack.pack == p).tuples()
      Faza.update({Faza.packed:1}).where(Faza.detail.in_(detail)).execute()
      DetailPack.delete().where(DetailPack.pack == p).execute()
      p.delete_instance(recursive=True)
      await message.answer(f'Пачка {pack} удалена')

    else:
      await message.answer(f'Пачки {pack} не существует')



# Запрос наличия нарядов на проверку ОТК
@dp.message_handler(commands=['otc'])
async def start(message):
  if Worker.select().join(User).where(User.telegram == message.chat.id,Worker.oper.in_(['otc','admin','director'])).first() != None:
    oper = {'paint': 'Покраска','weld':'Сварка'}
    text = ''
    otc_weld = Otc.select(Otc.detail).where(Otc.end == None,Otc.oper == 'weld',Otc.fix == 0).tuples()
    detail_weld = Detail.select().where(Detail.faza.in_(otc_weld),Detail.oper.in_(['weld']))
    otc_paint = Otc.select(Otc.detail).where(Otc.end == None,Otc.oper == 'paint',Otc.fix == 0).tuples()
    detail_paint = Detail.select().where(Detail.faza.in_(otc_paint),Detail.oper.in_(['paint']))

    # if len(detail) != 0:
    for d in detail_weld:
      text += f'{d.detail} {oper[d.oper]} {d.worker_1.user.surname}\n'
    for p in detail_paint:
      text += f'{p.detail} {oper[p.oper]} {p.worker_1.user.surname}\n'
    if text == '':
      text = 'Нет нарядов для проверки'
  else:
    text = 'Команда не доступна'
  await bot.send_message(message.from_user.id,text)
  connection.close()

@dp.message_handler(commands=['weight'])
async def start(message):
  point = Point.select(Point,fn.SUM(Drawing.weight).alias('we')).join(Drawing).where(Drawing.cas == 15).group_by(Point.name)
  text = ''
  for p in point:
    text += f'{p.name} {p.we}\n'
  await message.answer(text)
  connection.close()

@dp.message_handler(commands=['open','close'])
async def open(message):
  
  OpenDoor(message)

@dp.callback_query_handler(lambda message: message.data.startswith('otc ok '))
async def otc_callback(callback: types.CallbackQuery):
  text = callback.data.replace('otc ok ','').split(' ')
  text = {'id':text[0],'oper':text[1],'worker':text[2],'usc':int(text[3])}
  otc = Otc.get(Otc.id == int(text['id']))
  faza = otc.detail
  otc.end = datetime.today()
  otc.worker = int(text['worker'])
  if text['oper'] == 'paint':
    faza.packed = 1
  elif text['oper'] == 'weld':
    if text['usc'] == 1:
      otc.usc = True
    Detail.update({Detail.to_work: 1}).where(Detail.oper == 'paint',Detail.detail == otc.detail.detail).execute()
    faza.paint = 1
  otc.save()
  faza.save()
  await bot.send_message(callback.from_user.id,f'Наряд {faza.detail} прошел проверку')
  await callback.answer()
  await bot.delete_message(callback.from_user.id,callback.message.message_id)
  connection.close()

@dp.callback_query_handler(lambda message: message.data.startswith('otc cancel '))
async def otc_callback(callback: types.CallbackQuery):
  text = callback.data.replace('otc cancel ','').split(' ')
  text = {'id':text[0],'oper':text[1]}
  otc = Otc.get(Otc.id == int(text['id']))
  faza = otc.detail
  otc.fix = True
  otc.save()
  if text['oper'] == 'paint':
    faza.paint = 2
  elif text['oper'] == 'weld':
    faza.weld = 2
  faza.save()
  detail = Detail.select().where(Detail.detail == faza.detail,Detail.oper == text['oper']).first()
  detail.end = None
  detail.save()
  await bot.send_message(callback.from_user.id,f'Наряд {faza.detail} отправлен на доработку')
  await callback.answer()
  await bot.delete_message(callback.from_user.id,callback.message.message_id)
  connection.close()


# Запросы от администратора
# @dp.message_handler(lambda message: Group(message,['admi']), content_types=['photo','video'])
# async def chat(message: types.Message):
#   print(message)
#   await message.answer('Голос',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Hello',callback_data='kyky')))
#   await message.delete()
#   connection.close()


# Проверка ОТК
@dp.message_handler(lambda message: Group(message,['admin','otc']), content_types=['photo','video'])
async def otc_test(message):
  worker = Worker.select().join(User).where(Worker.oper.in_(['admin','otc']),User.telegram == message.chat.id).first()
  file_name = f'media/scaner/{message.chat.id}.jpg'
  await message.photo[-1].download(file_name)
  text = await Photo(message)
  if text[0] != 'Run':
    await message.answer('Неверный QR-код')
    await message.delete()
    return
  result = await OtcUser(message,text,worker.id)
  if type(result) == str:
    await message.answer(result)
  else:
    btn = InlineKeyboardMarkup(row_width=2)
    if result.oper == 'paint':
      btn.add(InlineKeyboardButton('Провести',callback_data=f'otc ok {result.id} {result.oper} {worker.id} 0'),
      InlineKeyboardButton('Вернуть на доработку',callback_data=f'otc cancel {result.id} {result.oper}'),
      # InlineKeyboardButton('Показать чертеж',callback_data=f'123')
      )
    else:
      btn.add(InlineKeyboardButton('Провести без УЗК',callback_data=f'otc ok {result.id} {result.oper} {worker.id} 0'),
      InlineKeyboardButton('Провести с УЗК',callback_data=f'otc ok {result.id} {result.oper} {worker.id} 1'),
      InlineKeyboardButton('Вернуть на доработку',callback_data=f'otc cancel {result.id} {result.oper}'),
      # InlineKeyboardButton('Показать чертеж',callback_data=f'123')
      )
    await message.answer('Действия с нарядом',reply_markup=btn)
  await message.delete()
  connection.close()

# Отправка Файла для бирок
@dp.message_handler(content_types=['document'])
async def handle_docs_document(message):
  print(message)
  if message.document.file_name == 'paint.xlsx':
    file_name = f'media/scaner/{message.chat.id}.xlsx'
    await message.document.download(file_name)
    result = Birk(file_name)
    await TechBirk(result)
  connection.close()



# Отправка Видео
@dp.message_handler(content_types=['video','photo'])
async def handle_docs_photo(message):
  result = await Photo(message)
  result = await Workers(message,result)
  await bot.send_message(message.from_user.id,result)
  await message.delete()
  connection.close()





@dp.message_handler()
async def start(message: types.Message):
  text = (message.text).split(' ')
  if text[0].lower() == 'марка':
    result = await Marka(text)

  elif message.text.lower().startswith('н '):
    result = await InfoDetail(text)

  elif text[0].lower() == 'reg' and message.chat.id == 365803624:
    result = await RegMan(text)

  elif text[0].lower() == 'user' and message.chat.id == 365803624:
    result = await UserAdd(message)
  else:
    result = 'Нет такой команды'

  await bot.send_message(message.from_user.id,result)
  await message.delete()
  connection.close()
executor.start_polling(dp,skip_updates=True)