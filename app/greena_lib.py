from models import *
import time
import random

def get_openid():
    return 'x'*28

def create_order():
    order = Order()
    order.order_id = time.strftime('%Y%m%d%H%M%s', time.localtime()) + str(random.randint(1000, 2000))
    return order
