# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class AssemblyNorm(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    name = CharField(max_length=250)
    mass_of = IntegerField()
    mass_to = IntegerField()
    count_of = IntegerField()
    count_to = IntegerField()
    complexity = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    norm = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    choice = CharField(max_length=100)
    class Meta:
        table_name = "assemblynorms"


@snapshot.append
class Order(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField(default=datetime.datetime.now)
    cas = CharField(max_length=50)
    color = CharField(max_length=30, null=True)
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
    assembly = snapshot.ForeignKeyField(backref='bolts', index=True, model='drawing')
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
    assembly = snapshot.ForeignKeyField(backref='parts', index=True, model='drawing')
    number = IntegerField()
    count = IntegerField()
    profile = CharField(max_length=100)
    size = CharField(max_length=100)
    width = CharField(default='', max_length=100)
    length = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    mark = CharField(max_length=50)
    manipulation = CharField(max_length=150)
    work = CharField(max_length=10)
    depth = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    perimeter = IntegerField(default=0)
    class Meta:
        table_name = "parts"


@snapshot.append
class Chamfer(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    part = snapshot.ForeignKeyField(backref='chamfers', index=True, model='part')
    length = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "chamfers"


@snapshot.append
class User(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    surname = CharField(max_length=100)
    name = CharField(max_length=100)
    patronymic = CharField(max_length=100)
    class Meta:
        table_name = "users"


@snapshot.append
class Worker(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    user = snapshot.ForeignKeyField(backref='workers', index=True, model='user')
    oper = CharField(max_length=100)
    oper_rus = CharField(max_length=100)
    class Meta:
        table_name = "workers"


@snapshot.append
class Detail(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    detail = IntegerField()
    basic = CharField(max_length=20)
    oper = CharField(max_length=20)
    worker = snapshot.ForeignKeyField(backref='details', index=True, model='worker', null=True)
    start = DateTimeField(null=True)
    end = DateTimeField(null=True)
    class Meta:
        table_name = "details"


@snapshot.append
class Hole(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    part = snapshot.ForeignKeyField(backref='holes', index=True, model='part')
    diameter = IntegerField()
    count = IntegerField()
    depth = IntegerField()
    class Meta:
        table_name = "holes"


@snapshot.append
class HoleNorm(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    depth_of = IntegerField()
    depth_to = IntegerField()
    diameter = IntegerField()
    lenght_of = IntegerField()
    lenght_to = IntegerField()
    count = IntegerField()
    norm = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    metal = CharField(max_length=15)
    class Meta:
        table_name = "holenorms"


@snapshot.append
class Nut(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(backref='nuts', index=True, model='drawing')
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
    assembly = snapshot.ForeignKeyField(backref='points', index=True, model='drawing')
    name = CharField(max_length=100)
    point_x = CharField(max_length=30)
    point_y = CharField(max_length=30)
    point_z = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    faza = IntegerField(null=True)
    line = IntegerField(null=True)
    in_work = BooleanField(default=False)
    draw = IntegerField(null=True)
    class Meta:
        table_name = "points"


@snapshot.append
class PointPart(peewee.Model):
    point = snapshot.ForeignKeyField(backref='pointparts', index=True, model='point')
    part = snapshot.ForeignKeyField(backref='pointparts', index=True, model='part')
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
    class Meta:
        table_name = "pointparts"


@snapshot.append
class SawNorm(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    profile = CharField(max_length=50)
    size = CharField(max_length=50)
    speed_saw = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    speed_feed = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    step_tooth = IntegerField(default=0)
    norm_direct = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    norm_oblique = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "sawnorms"


@snapshot.append
class Washer(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField()
    assembly = snapshot.ForeignKeyField(backref='washers', index=True, model='drawing')
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
    assembly = snapshot.ForeignKeyField(backref='welds', index=True, model='drawing')
    cathet = IntegerField()
    length = DecimalField(auto_round=False, decimal_places=3, max_digits=12, rounding='ROUND_HALF_EVEN')
    count = IntegerField()
    class Meta:
        table_name = "welds"


@snapshot.append
class WeldNorm(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    cathet = IntegerField()
    norm = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "weldnorms"


def forward(old_orm, new_orm):
    worker = new_orm['worker']
    return [
        # Apply default value '' to the field worker.oper_rus,
        worker.update({worker.oper_rus: ''}).where(worker.oper_rus.is_null(True)),
    ]
