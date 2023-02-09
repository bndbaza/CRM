from models import *

def post_metal(run):
    order = Order.get(Order.cas == run.case)
    index2 = NeedForMetal.select(NeedForMetal.id).where(NeedForMetal.case == order).tuples()
    index = []
    for i in index2:
        index.append(i[0])
    for i in run.run:
        if i.id == 0:
            NeedForMetal.create(catalog_steel=i.metal,weight=i.weight,case=order,name_steel=i.name_steel)
        else:
            index.remove(i.id)
    for i in index:
        NeedForMetal.delete().where(NeedForMetal.id == i).execute()
    



    return get_metal(order)

def get_metal(order):
    return NeedForMetal.select(
        CatalogSteel.full_name,
        CatalogSteel.size,
        CatalogSteel.mark,
        CatalogSteel.id.alias('metal'),
        NeedForMetal.name_steel,
        NeedForMetal.weight,
        NeedForMetal.buy,
        NeedForMetal.id,
        ).join(CatalogSteel).where(NeedForMetal.case == order).order_by(CatalogSteel.full_name).dicts()
    

