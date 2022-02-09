from openpyxl import load_workbook
from models import HoleNorm, SawNorm, AssemblyNorm

def NormExcel():
  # HoleNormExcel()
  # SawNormExcel()
  AssemblyNormExcel()

def HoleNormExcel():
  wb = load_workbook('VVL.xlsx',data_only=True)
  sheet = wb.get_sheet_by_name('Сверление')
  post = []
  for y in range(2,164):
    d = []
    for i in range(1,7):
      if i == 1:
        d.append((sheet.cell(row=y,column=i).value).split('-')[0])
        d.append((sheet.cell(row=y,column=i).value).split('-')[1])
      elif i == 2 and sheet.cell(row=y,column=i).value == 33:
        d.append(1000)
      elif i == 3 and sheet.cell(row=y,column=i).value == 'до 3':
        d.append(0)
        d.append(2999)
      elif i == 3 and sheet.cell(row=y,column=i).value == 'свыше 3':
        d.append(3000)
        d.append(30000)
      elif i == 3 and sheet.cell(row=y,column=i).value == 0:
        d.append(0)
        d.append(0)
      else:
        d.append(sheet.cell(row=y,column=i).value)
    post.append(d)
  HoleNorm.insert_many(post, fields=[HoleNorm.depth_of,HoleNorm.depth_to,HoleNorm.diameter,HoleNorm.lenght_of,HoleNorm.lenght_to,HoleNorm.count,HoleNorm.norm,HoleNorm.metal]).execute()


def SawNormExcel():
  wb = load_workbook('VVL.xlsx',data_only=True)
  sheet = wb.get_sheet_by_name('Пиление проката')
  post = []
  for y in range(2,160):
    d = []
    for i in range(1,7):
      if i == 1 and len((sheet.cell(row=y,column=i).value).strip().split(' ')) > 2:
        d.append((sheet.cell(row=y,column=i).value).strip().split(' ')[0] + ' ' + (sheet.cell(row=y,column=i).value).split(' ')[1])
        d.append((sheet.cell(row=y,column=i).value).strip().split(' ')[2])
      elif i == 1 and len((sheet.cell(row=y,column=i).value).strip().split(' ')) == 2:
        d.append((sheet.cell(row=y,column=i).value).strip().split(' ')[0])
        d.append((sheet.cell(row=y,column=i).value).strip().split(' ')[1])
      elif sheet.cell(row=y,column=i).value == None:
        d.append(0)
      else:
        d.append(sheet.cell(row=y,column=i).value)
    post.append(d)
  SawNorm.insert_many(post, fields=[SawNorm.profile,SawNorm.size,SawNorm.speed_saw,SawNorm.speed_feed,SawNorm.step_tooth,SawNorm.norm_direct,SawNorm.norm_oblique]).execute()


def AssemblyNormExcel():
  wb = load_workbook('VVL.xlsx',data_only=True)
  sheet = wb.get_sheet_by_name('Сборка (ЕНиР)')
  post = []
  for y in range(17,865):
    d = []
    for i in range(1,9):
      if sheet.cell(row=y,column=i).value == None:
        d.append('')
      else:
        d.append(sheet.cell(row=y,column=i).value)
    post.append(d)
  AssemblyNorm.insert_many(post, fields=[AssemblyNorm.name,AssemblyNorm.mass_of,AssemblyNorm.mass_to,AssemblyNorm.count_of,AssemblyNorm.count_to,AssemblyNorm.complexity,AssemblyNorm.norm,AssemblyNorm.choice]).execute()