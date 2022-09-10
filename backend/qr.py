import qrcode
import os
import shutil
from models import Worker
import asyncio

from send_bot import Tech

def QRAuth(detail,case,oper):
  data = 'A ' + str(detail) +' '+oper
  filename = 'QR/aut'+str(detail)+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename

def QRRun(detail,case,oper):
  data = 'Run ' + str(detail) +' '+oper+' '+case
  filename = 'QR/run'+str(detail)+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename


def QRUser(worker):
  data = 'U '+str(worker.id)
  filename = 'Users/'+data+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename

def QRTask(task):
  data = 'T '+str(task.id)
  filename = 'QR/task'+data+'.png'
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img.save(filename)
  return filename



def QRPack(i):
  data = 'P '+str(i)
  filename = 'QR/pack 1 '+data+'.png'
  img = qrcode.make(data)
  img.save(filename)
  # return filename

  filename2 = 'QR/pack 2 '+data+'.png'
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img.save(filename2)

  filename3 = 'QR/pack 3 '+data+'.png'
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill_color="black", back_color="white")
  img.save(filename3)
  return filename

def QRShip(i):
  data = 'S '+str(i)
  filename = 'QR/ship 1 '+data+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename
