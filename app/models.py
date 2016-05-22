from . import db
from . import login_manager
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    addresses = db.relationship('Address', backref='user')

    def __repr__(self):
        return '<User %r>' % self.open_id

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name


class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.Text)

class ProductType(db.Model):
    __tablename__='product_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='type', lazy='dynamic')

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
