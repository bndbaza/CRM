import cv2
from pyzbar.pyzbar import decode

def Scaner(file_name):
  img = cv2.imread(file_name)
  try:
    code = decode(img)[0].data.decode('utf-8')
  except:
    code = 'Код не распознан'
  return code

def Scaner2(file_name):
  cap = cv2.VideoCapture(file_name)
  camera = True
  try:
    while camera == True:
      success, frame = cap.read()
      for code in decode(frame):
        result = code.data.decode('utf-8')
        camera = False
  except:
    result = 'Код не распознан'
  return result