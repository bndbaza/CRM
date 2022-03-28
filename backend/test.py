from models import *

def AAA():
  # pp = PointPart.select(PointPart.detail).join(Point).join(Drawing).join(Order).where(Order.cas == '2325').tuples()
  # Detail.update({Detail.to_work: True}).where(Detail.oper == 'assembly',Detail.detail.in_(pp)).execute()
  # dd = Detail.select(Detail.detail).where(Detail.to_work == True,Detail.end != None).tuples()
  # Detail.update({Detail.to_work: True}).where(Detail.oper == 'weld',Detail.detail.in_(dd)).execute()

  tt = Detail.select(Detail.detail).where(Detail.to_work == True,Detail.oper == 'weld',Detail.end != None).tuples()
  Detail.update({Detail.to_work: True}).where(Detail.oper == 'paint',Detail.detail.in_(tt)).execute()
  # Detail.update({Detail.to_work: True}).where(Detail.start != None,Detail.oper.in_(['weld','paint'])).execute()
  # Detail.update({Detail.to_work: False}).execute()