import datetime
from email.policy import default
from peewee import Model, IntegerField, DateTimeField, CharField, ForeignKeyField, DecimalField, PrimaryKeyField, BooleanField, BigIntegerField
# from peewee import *
from db import connection

class ModelBase(Model):
    class Meta:
        database = connection

class Order(ModelBase):
  class Meta:
    table_name='orders'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField(default=datetime.datetime.now)
  cas = CharField(max_length=50)
  color = CharField(max_length=30, null=True)
  status = CharField(max_length=100, null=True)
  name = CharField(max_length=500,null=True)
  contract = CharField(max_length=500,null=True)
  customer = CharField(max_length=500,null=True)
  consignee = CharField(max_length=500,null=True)
  weight = DecimalField(max_digits=12,decimal_places=3,null=True)
  upload = CharField(max_length=10,null=True)
  inside = BooleanField(default=False)

  
class Drawing(ModelBase):
  class Meta:
    table_name='drawings'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  cas = ForeignKeyField(Order,backref='drawings')
  assembly = CharField(max_length=50)
  area = DecimalField(max_digits=12,decimal_places=3)
  count = IntegerField()
  weight = DecimalField(max_digits=12,decimal_places=3,null=True)
  more = DecimalField(max_digits=12,decimal_places=3,null=True)
  paint = CharField(max_length=40,default='1')

class Point(ModelBase):
  class Meta:
    table_name='points'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='points')
  name = CharField(max_length=100)
  point_x = CharField(max_length=30)
  point_y = CharField(max_length=30)
  point_z = DecimalField(max_digits=12, decimal_places=3)
  faza = IntegerField(null=True)
  line = IntegerField(null=True)
  in_work = BooleanField(default=False)
  draw = CharField(max_length=250,null=True)


class User(ModelBase):
  class Meta:
    table_name='users'
  id = PrimaryKeyField(null=False)
  surname = CharField(max_length=100)
  name = CharField(max_length=100)
  patronymic = CharField(max_length=100)
  telegram = BigIntegerField(null=True)
  username = CharField(max_length=100,null=True)
  ip = CharField(max_length=250,null=True)
  phone = IntegerField(null=True)

class Worker(ModelBase):
  class Meta:
    table_name='workers'
  id = PrimaryKeyField(null=False)
  user = ForeignKeyField(User,backref='workers')
  oper = CharField(max_length=100)
  oper_rus = CharField(max_length=100)

class Task(ModelBase):
  class Meta:
    table_name='tasks'
  id = PrimaryKeyField(null=False)
  task = IntegerField()
  oper = CharField(max_length=20)
  worker_1 = ForeignKeyField(Worker,backref='tasks_1',null=True)
  worker_2 = ForeignKeyField(Worker,backref='tasks_2',null=True)
  start = DateTimeField(null=True)
  end = DateTimeField(null=True)
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)
  faza = IntegerField()
  order = ForeignKeyField(Order,backref='tasks')

class Part(ModelBase):
  class Meta:
    table_name='parts'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='parts')
  number = IntegerField()
  count = IntegerField()
  profile = CharField(max_length=100)
  size = CharField(max_length=100)
  width = CharField(max_length=100,default='')
  length = DecimalField(max_digits=12,decimal_places=3)
  weight = DecimalField(max_digits=12,decimal_places=3)
  mark = CharField(max_length=50)
  manipulation = CharField(max_length=150)
  work = CharField(max_length=10)
  depth = DecimalField(max_digits=12,decimal_places=3,default=0)
  perimeter = IntegerField(default=0)
  sn = CharField(max_length=50,null=True)
  area = DecimalField(max_digits=12,decimal_places=3,default=0)

class WeldNorm(ModelBase):
  class Meta:
    table_name='weldnorms'
  id = PrimaryKeyField(null=False)
  cathet = IntegerField()
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)

class Weld(ModelBase):
  class Meta:
    table_name='welds'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='welds')
  cathet = ForeignKeyField(WeldNorm,backref='welds')
  length = DecimalField(max_digits=12,decimal_places=3)
  count = IntegerField()

class Bolt(ModelBase):
  class Meta:
    table_name='bolts'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='bolts')
  profile = CharField(max_length=100)
  count = IntegerField()
  gost = CharField(max_length=50)
  weight = DecimalField(max_digits=12,decimal_places=3)

class Nut(ModelBase):
  class Meta:
    table_name='nuts'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='nuts')
  profile = CharField(max_length=100)
  count = IntegerField()
  gost = CharField(max_length=50)
  weight = DecimalField(max_digits=12,decimal_places=3)

class Washer(ModelBase):
  class Meta:
    table_name='washers'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='washers')
  profile = CharField(max_length=100)
  count = IntegerField()
  gost = CharField(max_length=50)
  weight = DecimalField(max_digits=12,decimal_places=3)

class HoleNorm(ModelBase):
  class Meta:
    table_name='holenorms'
  id = PrimaryKeyField(null=False)
  depth_of = IntegerField()
  depth_to = IntegerField()
  diameter = IntegerField()
  lenght_of = IntegerField()
  lenght_to = IntegerField()
  count = IntegerField()
  count_to = IntegerField()
  norm = DecimalField(max_digits=12,decimal_places=3)
  metal = CharField(max_length=15)

class Hole(ModelBase):
  class Meta:
    table_name='holes'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  part = ForeignKeyField(Part,backref='holes')
  diameter = IntegerField()
  count = IntegerField()
  depth = IntegerField()
  norm = ForeignKeyField(HoleNorm,backref='holes',null=True)

class Chamfer(ModelBase):
  class Meta:
    table_name='chamfers'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  part = ForeignKeyField(Part,backref='chamfers')
  length = DecimalField(max_digits=12,decimal_places=3)

class PointPart(ModelBase):
  class Meta:
    table_name='pointparts'
  point = ForeignKeyField(Point,backref='pointparts')
  part = ForeignKeyField(Part,backref='pointparts')
  detail = IntegerField()
  cgm = IntegerField(default=0)
  saw = IntegerField(default=0)
  hole = IntegerField(default=0)
  bevel = IntegerField(default=0)
  notch = IntegerField(default=0)
  chamfer = IntegerField(default=0)
  milling = IntegerField(default=0)
  bend = IntegerField(default=0)
  weld = IntegerField(default=1)
  turning = IntegerField(default=0)
  joint = IntegerField(default=0)


class SawNorm(ModelBase):
  class Meta:
    table_name='sawnorms'
  id = PrimaryKeyField(null=False)
  profile = CharField(max_length=50)
  size = CharField(max_length=50)
  speed_saw = DecimalField(max_digits=12,decimal_places=3,default=0)
  speed_feed = DecimalField(max_digits=12,decimal_places=3,default=0)
  step_tooth = IntegerField(default=0)
  norm_direct = DecimalField(max_digits=12,decimal_places=3,default=0)
  norm_oblique = DecimalField(max_digits=12,decimal_places=3,default=0)

class AssemblyNorm(ModelBase):
  class Meta:
    table_name='assemblynorms'
  id = PrimaryKeyField(null=False)
  name = CharField(max_length=250)
  mass_of = IntegerField()
  mass_to = IntegerField()
  count_of = IntegerField()
  count_to = IntegerField()
  complexity = DecimalField(max_digits=12,decimal_places=3,default=0)
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)
  choice = CharField(max_length=100)



class Faza(ModelBase):
  class Meta:
    table_name='fazas'
  id = PrimaryKeyField(null=False)
  detail = IntegerField()
  faza = IntegerField(null=True)
  case = ForeignKeyField(Order,backref='details',null=True)
  weight = DecimalField(max_digits=12,decimal_places=3,default=0)
  area = DecimalField(max_digits=12,decimal_places=3,default=0)
  kmd = IntegerField(default=3)
  in_work = IntegerField(default=1)
  preparation = IntegerField(default=1)
  set = IntegerField(default=0)
  assembly = IntegerField(default=0)
  weld = IntegerField(default=0)
  paint = IntegerField(default=0)
  packed = IntegerField(default=0)
  shipment = IntegerField(default=0)
  in_object = IntegerField(default=0)
  mount = IntegerField(default=0)

class Detail(ModelBase):
  class Meta:
    table_name='details'
  id = PrimaryKeyField(null=False)
  detail = IntegerField()
  basic = CharField(max_length=20)
  oper = CharField(max_length=20)
  worker_1 = ForeignKeyField(Worker,backref='details_1',null=True)
  worker_2 = ForeignKeyField(Worker,backref='details_2',null=True)
  start = DateTimeField(null=True)
  end = DateTimeField(null=True)
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)
  to_work = BooleanField(default=False)
  faza = ForeignKeyField(Faza,backref='details')

class TaskPart(ModelBase):
  class Meta:
    table_name='taskparts'
  id = PrimaryKeyField(null=False)
  task = ForeignKeyField(Task,backref='taskparts',null=True)
  part = ForeignKeyField(Part,backref='taskparts',null=True)
  finish = BooleanField(default=False)
  count = IntegerField()

class PrintBirk(ModelBase):
  class Meta:
    table_name='printbirks'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField(default=datetime.datetime.now)
  detail = IntegerField()
  length = IntegerField()
  weight = DecimalField(max_digits=12,decimal_places=3,default=0)
  case = CharField(max_length=30)
  faza = IntegerField()
  mark = CharField(max_length=30)
  qr = CharField(max_length=40)
  count = IntegerField()
  draw = CharField()

class Stage(ModelBase):
  class Meta:
    table_name='stages'
  id = PrimaryKeyField(null=False)
  kmd = IntegerField(default=0)
  in_work = IntegerField(default=0)
  preparation = IntegerField(default=0)
  set = IntegerField(default=0)
  assembly = IntegerField(default=0)
  weld = IntegerField(default=0)
  paint = IntegerField(default=0)
  shipment = IntegerField(default=0)
  in_object = IntegerField(default=0)
  mount = IntegerField(default=0)

class DetailUser(ModelBase):
  class Meta:
    table_name='detailusers'
  id = PrimaryKeyField(null=False)
  detail = ForeignKeyField(Detail,backref='detailusers')
  worker = ForeignKeyField(Worker,backref='detailusers')
  weight = DecimalField(max_digits=12,decimal_places=3,default=0)
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)



class Shipment(ModelBase):
  class Meta:
    table_name='shipments'
  id = PrimaryKeyField(null=False)
  order = ForeignKeyField(Order,backref='shipments',null=True)
  number = IntegerField()
  date = DateTimeField(null=True)
  car = CharField(max_length=250)
  number_car = CharField(max_length=250)
  driver = CharField(max_length=250)
  ready = CharField(max_length=200,null=True)



class Packed(ModelBase):
  class Meta:
    table_name='packeds'
  id = PrimaryKeyField(null=False)
  number = IntegerField()
  size = CharField(max_length=150,null=True)
  shipment = ForeignKeyField(Shipment,backref='packeds',null=True)
  pack = CharField(max_length=50,null=True)
  date = DateTimeField(default=datetime.datetime.now)
  order = ForeignKeyField(Order,backref='packeds',null=True)
  ready = CharField(max_length=200,null=True)
  

  

class DetailPack(ModelBase):
  class Meta:
    table_name='detailpacks'
  id = PrimaryKeyField(null=False)
  detail = ForeignKeyField(Faza,backref='detailpacks')
  pack = ForeignKeyField(Packed,backref='detailpacks',null=True)


class Reg(ModelBase):
  class Meta:
    table_name='regs'
  id = PrimaryKeyField(null=False)
  surname = CharField(max_length=100)
  name = CharField(max_length=100)
  patronymic = CharField(max_length=100)
  telegram = BigIntegerField(null=True)
  username = CharField(max_length=100,null=True)
  user = ForeignKeyField(User,backref='regs',null=True)


# class TestTime(ModelBase):
#   class Meta:
#     table_name='testtimes'
#   id = PrimaryKeyField(null=False)
#   mark = CharField(max_length=100)
#   x = CharField(max_length=100)
#   y = CharField(max_length=100)
#   z = CharField(max_length=100)
#   name = CharField(max_length=100)
#   paint = IntegerField()
  
class Otc(ModelBase):
  class Meta:
    table_name='otcs'
  id = PrimaryKeyField(null=False)
  detail = ForeignKeyField(Faza,backref='otcs')
  worker = ForeignKeyField(Worker,backref='otcs',null=True)
  start = DateTimeField(default=datetime.datetime.now)
  end = DateTimeField(null=True)
  oper = CharField(max_length=100)
  error = IntegerField(default=0)
  usc = BooleanField(default=False)
  fix = BooleanField(default=False)
  
class Coating(ModelBase):
  class Meta:
    table_name='coatings'
  id = PrimaryKeyField(null=False)
  number = IntegerField()
  name = CharField(max_length=250)
  color = CharField(max_length=150)
  depth = DecimalField(max_digits=12,decimal_places=3,default=0)
  price = IntegerField()

class PointPaint(ModelBase):
  class Meta:
    table_name='pointpaints'
  id = PrimaryKeyField(null=False)
  coat = ForeignKeyField(Coating,backref='pointpaints')
  point = ForeignKeyField(Point,backref='pointpaints')
  number = CharField(max_length=150)

class Joint(ModelBase):
  class Meta:
    table_name='joints'
  id = PrimaryKeyField(null=False)
  paint = ForeignKeyField(Part,backref='joints')
  detail = ForeignKeyField(Detail,backref='joints')
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)

class JointNorm(ModelBase):
  class Meta:
    table_name='jointnorms'
  id = PrimaryKeyField(null=False)
  profile = CharField(max_length=150)
  size_of = IntegerField()
  size_to = IntegerField()
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)

class CatalogSteel(ModelBase):
  class Meta:
    table_name='catalogsteels'
  id = PrimaryKeyField(null=False)
  name = CharField(max_length=100)
  full_name = CharField(max_length=200)
  size = CharField(max_length=100)
  mark = CharField(max_length=100)
  gost = CharField(max_length=100)
  width = BooleanField()
  weight = DecimalField(max_digits=12,decimal_places=3,default=0)

class StoreSteel(ModelBase):
  class Meta:
    table_name='storesteels'
  id = PrimaryKeyField(null=False)
  catalog_steel = ForeignKeyField(CatalogSteel,backref='storesteels')
  width = IntegerField()
  length = IntegerField()
  name_steel = CharField(max_length=100)
  price = DecimalField(max_digits=12,decimal_places=3,default=0)
  receipt_date = DateTimeField(default=datetime.datetime.now)
  vendor = CharField(max_length=200)
  shop = BooleanField(default=False)

class NeedForMetal(ModelBase):
  class Meta:
    table_name='needformetals'
  id = PrimaryKeyField(null=False)
  catalog_steel = ForeignKeyField(CatalogSteel,backref='needformetals')
  name_steel = CharField(max_length=100,null=True)
  receipt_date = DateTimeField(default=datetime.datetime.now)
  case = ForeignKeyField(Order,backref='needformetals')
  buy = BooleanField(default=False)
  weight = DecimalField(max_digits=12,decimal_places=3,default=0)

class CallList(ModelBase):
  class Meta:
    table_name='calllists'
  id = PrimaryKeyField(null=False)
  inbound = CharField(max_length=100)
  date_in = DateTimeField()
  outgoing = CharField(max_length=100)
  date_out = DateTimeField(null=True)
  record = CharField(max_length=150,null=True)

class PhoneBook(ModelBase):
  class Meta:
    table_name='phonebooks'
  id = PrimaryKeyField(null=False)
  company = CharField(max_length=100,null=True)
  surname = CharField(max_length=100,null=True)
  name = CharField(max_length=100,null=True)
  patronymic = CharField(max_length=100,null=True)
  phone = CharField(max_length=50)
  direction = CharField(max_length=50)
