from typing import Optional, List, Dict
from pydantic import BaseModel
import datetime

from pydantic.types import constr

from models import Drawing


class Base(BaseModel):
  id: int
  create_date: datetime.datetime

  class Config:
    orm_mode = True

class DrawingBase(BaseModel):
  id: int
  create_date: datetime.datetime
  # cas: Optional[OrderBase]
  assembly: str
  area: float
  count: int
  weight: float
  more: float

  class Config:
    orm_mode = True

class OrderBase(Base):
  cas: str
  # drawings: List[DrawingBase]


  


class PointBase(Base):
  assembly: Optional[DrawingBase]
  point_x:str
  point_y: str
  point_z: float
  faza: int
  line: int


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