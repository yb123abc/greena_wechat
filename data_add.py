#coding=utf-8
from app.models import Product,ProductType
from app import db

def add_product_type(db):
    pt1 = ProductType()
    pt1.name = u'汉堡系列'
    pt1.description = u'被面包包裹的健康'

    pt2 = ProductType()
    pt2.name = u'面条系列'
    pt2.description = u'爽滑入味的健康'

    pt3 = ProductType()
    pt3.name = u'沙拉系列'
    pt3.description = u'冷拌的美味健康'

    db.session.add(pt1)
    db.session.add(pt2)
    db.session.add(pt3)
    db.session.commit()

def add_product(db):
    type1 = ProductType.query.filter_by(id=1).first()
    product1 = Product()
    product1.name = u'鸡肉汉堡'
    product1.description = u'美味的xxx汉堡诱惑你的味蕾'
    product1.type=type1
    product1.price=20

    product2 = Product()
    product2.name = u'牛肉汉堡'
    product2.description = u'美味的xxx汉堡诱惑你的味蕾'
    product2.type=type1
    product2.price=25

    product3 = Product()
    product3.name = u'蔬菜汉堡'
    product3.description = u'美味的xxx汉堡诱惑你的味蕾'
    product3.type=type1
    product3.price=30

    type2 = ProductType.query.filter_by(id=2).first()
    product4 = Product()
    product4.name = u'泰式面条'
    product4.description = u'美味的xxx面条诱惑你的味蕾'
    product4.type=type2
    product4.price=25

    product5 = Product()
    product5.name = u'川辣面条'
    product5.description = u'美味的xxx面条诱惑你的味蕾'
    product5.type=type2
    product5.price=30

    product6 = Product()
    product6.name = u'韩式面条'
    product6.description = u'美味的xxx面条诱惑你的味蕾'
    product6.type=type2
    product6.price=25

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    db.session.add(product6)
    db.session.commit()

def add_role():
    wechat_role = Role()
    wechat_role.name = u'微信用户'
    db.session.add(wechat_role)
    db.session.commit()
