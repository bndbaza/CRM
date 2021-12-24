import datetime
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

class Part(ModelBase):
  class Meta:
    table_name='parts'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,backref='parts')
  number = IntegerField()
  count = IntegerField()
  profile = CharField(max_length=100)
  length = DecimalField(max_digits=12,decimal_places=3)
  weight = DecimalField(max_digits=12,decimal_places=3)
  mark = CharField(max_length=50)
  manipulation = CharField(max_length=150)

class Weld(ModelBase):
  class Meta:
    table_name='welds'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,related_name='welds')
  cathet = IntegerField()
  length = DecimalField(max_digits=12,decimal_places=3)
  count = IntegerField()

class Bolt(ModelBase):
  class Meta:
    table_name='bolts'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,related_name='bolts')
  profile = CharField(max_length=100)
  count = IntegerField()
  gost = CharField(max_length=50)
  weight = DecimalField(max_digits=12,decimal_places=3)

class Nut(ModelBase):
  class Meta:
    table_name='nuts'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,related_name='nuts')
  profile = CharField(max_length=100)
  count = IntegerField()
  gost = CharField(max_length=50)
  weight = DecimalField(max_digits=12,decimal_places=3)

class Washer(ModelBase):
  class Meta:
    table_name='washers'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  assembly = ForeignKeyField(Drawing,related_name='washers')
  profile = CharField(max_length=100)
  count = IntegerField()
  gost = CharField(max_length=50)
  weight = DecimalField(max_digits=12,decimal_places=3)

class Hole(ModelBase):
  class Meta:
    table_name='holes'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  part = ForeignKeyField(Part,related_name='holes')
  diameter = IntegerField()
  count = IntegerField()
  depth = IntegerField()

class Chamfer(ModelBase):
  class Meta:
    table_name='chamfers'
  id = PrimaryKeyField(null=False)
  create_date = DateTimeField()
  part = ForeignKeyField(Part,related_name='chamfers')
  length = DecimalField(max_digits=12,decimal_places=3)

class PointPart(ModelBase):
  class Meta:
    table_name='pointparts'
  point = ForeignKeyField(Point)
  part = ForeignKeyField(Part)
  detail = IntegerField()
  cgm = IntegerField(default=0)
  saw = IntegerField(default=0)
  hole = IntegerField(default=0)
  bevel = IntegerField(default=0)
  notch = IntegerField(default=0)
  chamfer = IntegerField(default=0)
  milling = IntegerField(default=0)
  bend = IntegerField(default=0)
