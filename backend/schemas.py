from typing import Optional, List, Dict
from pydantic import BaseModel
import datetime


class Base(BaseModel):
  id: int
  create_date: datetime.datetime

  class Config:
    orm_mode = True


class OrderBase(Base):
  cas: str


class DrawingBase(Base):
  id: int
  create_date: datetime.datetime
  cas: Optional[OrderBase]
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
  # line: int


class PartBase(Base):
  assembly: Optional[DrawingBase]
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
  point: Optional[PointBase]
  part: Optional[PartBase]
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
  norm: float

  class Config:
    orm_mode = True

class TaskBase(BaseModel):
  id: int
  task: int
  oper: str
  worker: WorkerBase | None = None
  start: datetime.datetime
  norm: float

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