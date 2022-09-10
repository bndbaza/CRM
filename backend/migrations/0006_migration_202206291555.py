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
    status = CharField(max_length=100, null=True)
    name = CharField(max_length=500, null=True)
    contract = CharField(max_length=500, null=True)
    customer = CharField(max_length=500, null=True)
    consignee = CharField(max_length=500, null=True)
    weight = DecimalField(auto_round=False, decimal_places=3, max_digits=12, null=True, rounding='ROUND_HALF_EVEN')
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
    sn = CharField(max_length=50, null=True)
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
class Coating(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    number = IntegerField()
    name = CharField(max_length=250)
    color = CharField(max_length=150)
    depth = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "coatings"


@snapshot.append
class User(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    surname = CharField(max_length=100)
    name = CharField(max_length=100)
    patronymic = CharField(max_length=100)
    telegram = BigIntegerField(null=True)
    username = CharField(max_length=100, null=True)
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
class Faza(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    detail = IntegerField()
    faza = IntegerField(null=True)
    case = snapshot.ForeignKeyField(backref='details', index=True, model='order', null=True)
    weight = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
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
    class Meta:
        table_name = "fazas"


@snapshot.append
class Detail(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    detail = IntegerField()
    basic = CharField(max_length=20)
    oper = CharField(max_length=20)
    worker_1 = snapshot.ForeignKeyField(backref='details_1', index=True, model='worker', null=True)
    worker_2 = snapshot.ForeignKeyField(backref='details_2', index=True, model='worker', null=True)
    start = DateTimeField(null=True)
    end = DateTimeField(null=True)
    norm = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    to_work = BooleanField(default=False)
    faza = snapshot.ForeignKeyField(backref='details', index=True, model='faza', null=True)
    class Meta:
        table_name = "details"


@snapshot.append
class Shipment(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    order = snapshot.ForeignKeyField(backref='packeds', index=True, model='order', null=True)
    number = IntegerField()
    date = DateTimeField(default=datetime.datetime.now)
    car = CharField(max_length=250)
    ready = CharField(max_length=200, null=True)
    class Meta:
        table_name = "shipments"


@snapshot.append
class Packed(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    number = IntegerField()
    size = CharField(max_length=150, null=True)
    shipment = snapshot.ForeignKeyField(backref='packeds', index=True, model='shipment', null=True)
    pack = CharField(max_length=50, null=True)
    date = DateTimeField(default=datetime.datetime.now)
    order = snapshot.ForeignKeyField(backref='packeds', index=True, model='order', null=True)
    ready = CharField(max_length=200, null=True)
    class Meta:
        table_name = "packeds"


@snapshot.append
class DetailPack(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    detail = snapshot.ForeignKeyField(backref='detailpacks', index=True, model='faza')
    pack = snapshot.ForeignKeyField(backref='detailpacks', index=True, model='packed', null=True)
    class Meta:
        table_name = "detailpacks"


@snapshot.append
class DetailUser(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    detail = snapshot.ForeignKeyField(backref='detailusers', index=True, model='detail')
    worker = snapshot.ForeignKeyField(backref='detailusers', index=True, model='worker')
    weight = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    norm = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    class Meta:
        table_name = "detailusers"


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
class Otc(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    detail = snapshot.ForeignKeyField(backref='otcs', index=True, model='faza')
    worker = snapshot.ForeignKeyField(backref='otcs', index=True, model='worker', null=True)
    start = DateTimeField(default=datetime.datetime.now)
    end = DateTimeField(null=True)
    oper = CharField(max_length=100)
    error = IntegerField(default=0)
    usc = BooleanField(default=False)
    fix = BooleanField(default=False)
    class Meta:
        table_name = "otcs"


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
    draw = CharField(max_length=250, null=True)
    class Meta:
        table_name = "points"


@snapshot.append
class PointPaint(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    coat = snapshot.ForeignKeyField(backref='pointpaints', index=True, model='coating')
    point = snapshot.ForeignKeyField(backref='pointpaints', index=True, model='point')
    number = CharField(max_length=150)
    price = IntegerField()
    class Meta:
        table_name = "pointpaints"


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
    joint = IntegerField(default=0)
    class Meta:
        table_name = "pointparts"


@snapshot.append
class PrintBirk(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    create_date = DateTimeField(default=datetime.datetime.now)
    detail = IntegerField()
    length = IntegerField()
    weight = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    case = CharField(max_length=30)
    faza = IntegerField()
    mark = CharField(max_length=30)
    qr = CharField(max_length=40)
    count = IntegerField()
    draw = CharField(max_length=255)
    class Meta:
        table_name = "printbirks"


@snapshot.append
class Reg(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    surname = CharField(max_length=100)
    name = CharField(max_length=100)
    patronymic = CharField(max_length=100)
    telegram = BigIntegerField(null=True)
    username = CharField(max_length=100, null=True)
    user = snapshot.ForeignKeyField(backref='regs', index=True, model='user', null=True)
    class Meta:
        table_name = "regs"


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
class Task(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    task = IntegerField()
    oper = CharField(max_length=20)
    worker_1 = snapshot.ForeignKeyField(backref='tasks_1', index=True, model='worker', null=True)
    worker_2 = snapshot.ForeignKeyField(backref='tasks_2', index=True, model='worker', null=True)
    start = DateTimeField(null=True)
    end = DateTimeField(null=True)
    norm = DecimalField(auto_round=False, decimal_places=3, default=0, max_digits=12, rounding='ROUND_HALF_EVEN')
    faza = IntegerField()
    order = snapshot.ForeignKeyField(backref='tasks', index=True, model='order')
    class Meta:
        table_name = "tasks"


@snapshot.append
class TaskPart(peewee.Model):
    id = PrimaryKeyField(primary_key=True)
    task = snapshot.ForeignKeyField(backref='taskparts', index=True, model='task', null=True)
    part = snapshot.ForeignKeyField(backref='taskparts', index=True, model='part', null=True)
    finish = BooleanField(default=False)
    count = IntegerField()
    class Meta:
        table_name = "taskparts"


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


