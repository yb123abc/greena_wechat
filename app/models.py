from . import db
from . import login_manager
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    addresses = db.relationship('Address', backref='user')
    orders = db.relationship('Order', backref='user')
    address_default_id = db.Column(db.Integer)
    def __repr__(self):
        return '<User %s>' % self.open_id

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %s>' % self.name


class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    order_products = db.relationship('OrderProduct', backref='product', lazy='dynamic')
    def __repr__(self):
        return '<Product %s>' % self.name

class ProductType(db.Model):
    __tablename__='product_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='type', lazy='dynamic')
    def __repr__(self):
        return '<ProductType %s>' % self.name


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    province = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(64), nullable=False)
    reciplents = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    def __repr__(self):
        return '<Address %s>' % self.id


class Province(db.Model):
    __tablename__ = 'provinces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    citys = db.relationship('City', backref='province', lazy='dynamic')

class City(db.Model):
    __tablename__ = 'citys'
    id = db.Column(db.Integer, primary_key=True)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    name = db.Column(db.String(64), nullable=False)
    districts = db.relationship('District', backref='city', lazy='dynamic')

class District(db.Model):
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('citys.id'))
    name = db.Column(db.String(64), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_products = db.relationship('OrderProduct', backref='order', lazy='dynamic')
    total_sum = db.Column(db.Float, nullable=False, default=0)
    #address info
    province = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(128), nullable=False)
    zip_code = db.Column(db.String(64), nullable=False)
    reciplents = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    #order comment
    comment = db.Column(db.Text)
    #deliver time
    order_datetime = db.Column(db.DateTime)
    deliver_date = db.Column(db.Date)
    deliver_time = db.Column(db.Integer, default=0)
    #order status
    order_status = db.Column(db.Integer, default=0)
    shipping_status = db.Column(db.Integer, default=0)
    pay_status = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<order %s>' % self.order_id


class OrderProduct(db.Model):
    __tablename__ = 'order_products'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(64), db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    count = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<OrderProduct %s_%s>' % (self.order_id, product_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
