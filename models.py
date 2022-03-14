import datetime
from email.policy import default
from xmlrpc.server import CGIXMLRPCRequestHandler
from peewee import Model, IntegerField, DateTimeField, CharField, ForeignKeyField, DecimalField, PrimaryKeyField, BooleanField
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
  draw = IntegerField(null=True)

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

class Weld(ModelBase):
  class Meta:
    table_name='welds'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='welds')
  cathet = IntegerField()
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

class Hole(ModelBase):
  class Meta:
    table_name='holes'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  part = ForeignKeyField(Part,backref='holes')
  diameter = IntegerField()
  count = IntegerField()
  depth = IntegerField()

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
  norm = DecimalField(max_digits=12,decimal_places=3)
  metal = CharField(max_length=15)

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

class WeldNorm(ModelBase):
  class Meta:
    table_name='weldnorms'
  id = PrimaryKeyField(null=False)
  cathet = IntegerField()
  norm = DecimalField(max_digits=12,decimal_places=3,default=0)

class User(ModelBase):
  class Meta:
    table_name='users'
  id = PrimaryKeyField(null=False)
  surname = CharField(max_length=100)
  name = CharField(max_length=100)
  patronymic = CharField(max_length=100)

class Worker(ModelBase):
  class Meta:
    table_name='workers'
  id = PrimaryKeyField(null=False)
  user = ForeignKeyField(User,backref='workers')
  oper = CharField(max_length=100)
  oper_rus = CharField(max_length=100)

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


class TaskPart(ModelBase):
  class Meta:
    table_name='taskparts'
  id = PrimaryKeyField(null=False)
  task = ForeignKeyField(Task,backref='taskparts')
  part = ForeignKeyField(Part,backref='taskparts')
  finish = BooleanField(default=False)
