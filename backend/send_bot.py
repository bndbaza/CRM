from aiogram import Bot
from db import connection,bot_id, telega
from models import *
import asyncio



async def Bots(text):
  bot = Bot(bot_id)
  workers = Worker.select().where(Worker.oper.in_(['shipment']))
  for worker in workers:
    print(worker.user.telegram)
    await bot.send_message(worker.user.telegram,text)
  bot.close()

async def Viktor(text):
  bot = Bot(bot_id)
  await bot.send_message(365803624,text)
  bot.close()

async def Tech(text):
  bot = Bot(bot_id)
  file = open(text,"rb")
  await bot.send_document(telega,file) # 762167162 Вера
  bot.close()

async def ViktorDocs(text):
  bot = Bot(bot_id)
  file = open(text,"rb")
  await bot.send_document(365803624,file)
  bot.close()

async def TechBirk(text):
  bot = Bot(bot_id)
  file = open(text,"rb")
  await bot.send_document(765340311,file)
  bot.close()

async def Report(id,text):
  bot = Bot(bot_id)
  await bot.send_message(id,text)
  bot.close()

async def AllReport(users,text):
  bot = Bot(bot_id)
  for user in users:
    await bot.send_message(user[0],text)
  bot.close()
