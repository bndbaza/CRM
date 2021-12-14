# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Order(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField(default=datetime.datetime.now)
    cas = CharField(max_length=50)
    class Meta:
        table_name = "orders"


@snapshot.append
class Drawing(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    cas = snapshot.ForeignKeyField(backref='drawings', index=True, model='order')
    assembly = CharField(max_length=50)
    area = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    count = IntegerField()
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, null=True, rounding='ROUND_HALF_EVEN')
    more = DecimalField(auto_round=False, decimal_places=3, max_digits=12, null=True, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "drawings"


@snapshot.append
class Bolt(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(index=True, model='drawing')
    profile = CharField(max_length=100)
    count = IntegerField()
    gost = CharField(max_length=50)
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "bolts"


@snapshot.append
class Part(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(index=True, model='drawing')
    number = IntegerField()
    count = IntegerField()
    profile = CharField(max_length=100)
    length = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    mark = CharField(max_length=50)
    manipulation = CharField(max_length=150)
    class Meta:
        table_name = "parts"


@snapshot.append
class Chamfer(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    part = snapshot.ForeignKeyField(index=True, model='part')
    length = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "chamfers"


@snapshot.append
class Hole(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    part = snapshot.ForeignKeyField(index=True, model='part')
    diameter = IntegerField()
    count = IntegerField()
    depth = IntegerField()
    class Meta:
        table_name = "holes"


@snapshot.append
class Nut(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(index=True, model='drawing')
    profile = CharField(max_length=100)
    count = IntegerField()
    gost = CharField(max_length=50)
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "nuts"


@snapshot.append
class Point(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(index=True, model='drawing')
    point_x = CharField(max_length=30)
    point_y = CharField(max_length=30)
    point_z = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    faza = IntegerField(null=True)
    line = IntegerField(null=True)
    class Meta:
        table_name = "points"


@snapshot.append
class Washer(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(index=True, model='drawing')
    profile = CharField(max_length=100)
    count = IntegerField()
    gost = CharField(max_length=50)
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "washers"


@snapshot.append
class Weld(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(index=True, model='drawing')
    cathet = IntegerField()
    length = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    count = IntegerField()
    class Meta:
        table_name = "welds"


