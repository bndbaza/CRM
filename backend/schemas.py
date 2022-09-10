from typing import Any, List, Union
from typing import Optional, List, Dict
from pydantic import BaseModel
import datetime

import peewee
from pydantic.utils import GetterDict

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class Base(BaseModel):
  id: int
  create_date: datetime.datetime

  class Config:
    orm_mode = True


class OrderBase(Base):
  id: int
  cas: str
  create_date: datetime.datetime
  color: str | None = None
  status: str | None = None
  name: str | None = None
  contract: str | None = None
  customer: str | None = None
  consignee: str | None = None


class DrawingBase(Base):
  id: int
  create_date: datetime.datetime
  cas: OrderBase
  assembly: str
  area: float
  count: int
  weight: float
  more: float
  

class PointBase(Base):
  assembly: Optional[DrawingBase]
  point_x:str
  point_y: str
  point_z: float
  faza: int
  draw: str


class PartBase(Base):
  assembly: DrawingBase
  number: int
  count: int
  profile: str
  length: float
  weight: float
  mark: str
  manipulation: str


class WeldBase(Base):
  assembly: Optional[DrawingBase]
  cathet: int
  length: float
  count: int


class BoltBase(Base):
  assembly: Optional[DrawingBase]
  profile: str
  count: int
  gost: str
  weight: float


class NutBase(Base):
  assembly: Optional[DrawingBase]
  profile: str
  count: int
  gost: str
  weight: float


class WasherBase(Base):
  assembly: Optional[DrawingBase]
  profile: str
  count: int
  gost: str
  weight: float


class HoleBase(Base):
  part: Optional[PartBase]
  diameter: int
  count: int
  depth: int


class ChamferBase(Base):
  part: Optional[PartBase]
  length: float

class PointPartBase(BaseModel):
  id: int
  point: PointBase
  part: PartBase
  detail: int
  cgm: int
  saw: int
  hole: int
  bevel: int
  notch: int
  chamfer: int
  milling: int
  bend: int
  weld: int

  class Config:
    orm_mode = True

class FazaBase(BaseModel):
  faza: int
  aaa: Optional[float]

  class Config:
    orm_mode = True


class UserBase(BaseModel):
  id: int
  surname: str
  name: str
  patronymic: str

  class Config:
    orm_mode = True

class WorkerBase(BaseModel):
  id: int
  user: UserBase | None = None
  oper: str
  oper_rus: str

  class Config:
    orm_mode = True


class BasicDetailBase(BaseModel):
  id: int
  basic: str
  oper: str
  detail: int
  worker_1: WorkerBase | None = None
  worker_2: WorkerBase | None = None
  start: datetime.datetime | None = None
  end: datetime.datetime | None = None
  norm: float
  to_work: int

  class Config:
    orm_mode = True

class TerminalBase(BaseModel):
  saw: List[BasicDetailBase] | None = None
  assembly: List[BasicDetailBase] | None = None
  # finish: List[BasicDetailBase] | None = None
  
  class Config:
    orm_mode = True

class TaskBase(BaseModel):
  id: int
  task: int
  oper: str
  worker_1: WorkerBase | None = None
  worker_2: WorkerBase | None = None
  start: datetime.datetime | None = None
  end: datetime.datetime | None = None
  norm: float

  class Config:
    orm_mode = True

class TaskPartBase(BaseModel):
  id: int
  task: TaskBase
  part: PartBase
  count: int
  finish: int

  class Config:
    orm_mode = True


class BasicDetailBase1(BaseModel):
  error: str | None = None
  worker: List[WorkerBase]
  detail: List[BasicDetailBase] | List[TaskBase]

  class Config:
    orm_mode = True




class DetailBase(BaseModel):
  id: str
  user: str

  class Config:
    orm_mode = True

class DetailBase1(BaseModel):
  detail: str
  user: List[WorkerBase]

  class Config:
    orm_mode = True

class GoWork(BaseModel):
  detail: str
  user: List[WorkerBase]

  class Config:
    orm_mode = True

class ShipmentBase1(BaseModel):
  id: int
  number: int
  date: datetime.datetime | None = None
  car: str
  number_car: str
  ready: str | None = None
  driver: str

  class Config:
    orm_mode = True
    getter_dict = PeeweeGetterDict

class PackedBase(BaseModel):
  id: int | None = None
  number: int | None = None
  size: str | None = None
  pack: str | None = None
  shipment: ShipmentBase1 | None = None
  date: datetime.datetime | None = None
  order: OrderBase | None = None
  ready: str | None = None

  class Config:
    orm_mode = True

class PackedBaseAll(BaseModel):
  pack: PackedBase | None = None

  class Config:
    orm_mode = True
    getter_dict = PeeweeGetterDict

class ShipmentBase(BaseModel):
  id: int
  number: int
  date: datetime.datetime | None = None
  packeds: List[PackedBase] = []
  car: str
  number_car: str
  ready: str | None = None
  driver: str

  class Config:
    orm_mode = True
    getter_dict = PeeweeGetterDict


class OneDetailBase(BaseModel):
  pointparts: List[PointPartBase]
  details: List[BasicDetailBase]
  tasks: List[TaskPartBase]
  pack: PackedBase | None = None
  # ship: ShipmentBase | None = None

  class Config:
    orm_mode =True

class FazaReport(BaseModel):
  faza: float
  weight_kmd: float
  weight_in_work: float
  weight_preparation: float
  weight_set: float
  weight_assembly: float
  weight_weld: float
  weight_paint: float
  weight_packed: float
  weight_shipment: float
  weight_in_object: float
  weight_mount: float
  
  class Config:
    orm_mode = True

  

class OtcBase(BaseModel):
  id: int
  detail: FazaBase | None = None
  worker: WorkerBase | None = None
  start: datetime.datetime
  end: datetime.datetime
  oper: str
  error: int

  class Config:
    orm_mode = True

class BasicDetailBase2(BaseModel):
  in_job: List[BasicDetailBase] | None = None
  from_job: List[BasicDetailBase] | None = None
  no_job: List[BasicDetailBase] | None = None
  otc: List[OtcBase] | None = None

  
  class Config:
    orm_mode = True



class AllReport(BaseModel):
  weight_kmd: float
  weight_in_work: float
  weight_weld: float
  weight_paint: float
  weight_packed: float
  weight_shipment: float
  weight_mount: float
  weight_order: float
  
  class Config:
    orm_mode = True

class WeldNormBase(BaseModel):
  cathet: int
  norm: float


  class Config:
    orm_mode = True

class WeldUserBase(BaseModel):
  cathet: WeldNormBase
  length: int


  class Config:
    orm_mode = True

class DetailUserBase(BaseModel):
  detail: BasicDetailBase
  worker: WorkerBase
  weight_all: float
  norm_all: str | None = None
  weld: List[WeldUserBase] | None = None
  
  class Config:
    orm_mode = True


class DetailUserBaseAll(BaseModel):
  assembly: List[DetailUserBase]
  weld: List[DetailUserBase]

  class Config:
    orm_mode = True


class StageBase(BaseModel):
  id: int
  detail: int
  faza: int
  kmd: int
  in_work: int
  preparation: int
  set: int
  assembly: int
  weld: int
  paint: int
  packed: int
  shipment: int
  in_object: int
  mount: int
  weight: float
  color: str | None = None
  # case: OrderBase

  class Config:
    orm_mode = True


class CarBase(BaseModel):
  car: str
  number_car: str
  driver: str
  case: str

  class Config:
    orm_mode = True
    getter_dict = PeeweeGetterDict

class CarPostBase(BaseModel):
  car: CarBase | None = None

  class Config:
    orm_mode = True
    getter_dict = PeeweeGetterDict