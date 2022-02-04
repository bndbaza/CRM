import qrcode
import os
import shutil

def QRAuth(detail,case,oper):
  try:
    os.mkdir('QR')
  except:
    pass
  data = 'A ' + str(detail) +' '+oper
  filename = 'QR/aut'+oper+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename

def QRRun(detail,case,oper):
  try:
    os.mkdir('QR')
  except:
    pass
  data = 'Run ' + str(detail) +' '+oper+' '+case
  filename = 'QR/run'+oper+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename

def Delpng():
  try:
    shutil.rmtree('QR')
  except:
    pass

def QRUser(id):
  data = 'U '+str(id)
  filename = 'Users/'+data+'.png'
  img = qrcode.make(data)
  img.save(filename)
  return filename
