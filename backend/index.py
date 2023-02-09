from models import *
import random


def get_orders():
    orders = Order.select().where(Order.status != None).order_by(Order.status,Order.inside)
    for order in orders:
        finish = 0
        fazas = Faza.select().where(Faza.case == order.id)
        for faza in fazas:
            if faza.kmd == 3:
                finish += faza.weight
            if faza.in_work == 3:
                finish += faza.weight
            if faza.weld == 3:
                finish += faza.weight
            if faza.paint == 3:
                finish += faza.weight
            if faza.packed == 3:
                finish += faza.weight
            if faza.shipment == 3:
                finish += faza.weight
        order.finish = int(finish / (order.weight*6) * 100)
    return orders

def get_color(inside):
    colors = ['red','pink','purple','deep-purple',
            'indigo','blue','cyan','teal',
            'green','lime','yellow','amber','orange','deep-orange','brown','blue-grey']
    if inside:
        return 'grey'
    else:
        order_colors = Order.select().where(Order.status == 'В работе',Order.inside == False).group_by(Order.color)
        for oc in order_colors:
            colors.remove(oc.color)
        color = random.choice(colors)
        return color
