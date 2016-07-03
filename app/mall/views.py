#coding:utf-8
from flask import render_template,request, url_for, redirect
from flask.ext.login import login_required, current_user
from . import mall
from .. import db
from ..models import Product, ProductType, Address, Province, City, District, Order, OrderProduct
from forms import AddressForm
import json
import urllib
import datetime
from .. import greena_lib

@mall.route('/product/<int:id>')
@login_required
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@mall.route('/shopping_cart')
@login_required
def shopping_cart():
    user = current_user._get_current_object()
    address_id = request.args.get('address_id', user.address_default_id, type=int)
    address = Address.query.get(address_id)
        
    if address and address not in user.addresses:
        address = None

    cart_cookie = request.cookies.get('shopping_cart', None)
    products = []
    total_sum = 0
    if cart_cookie:
        cart_cookie = urllib.unquote(cart_cookie)
        shopping_cart = json.loads(cart_cookie)
        for cart_row in shopping_cart:
            product = Product.query.get_or_404(cart_row['id'])
            products.append([product, cart_row['count']])
            total_sum += product.price * cart_row['count']

    empty_cart = True if len(products)==0 else False

    return render_template('shopping_cart.html', products=products, empty_cart=empty_cart, total_sum=total_sum, address=address)

@mall.route('/user')
@login_required
def user_center():
    return render_template('user_center.html', user=current_user)

@mall.route('/address')
@login_required
def address():
    user = current_user._get_current_object()
    id = user.id
    address_default_id = user.address_default_id
    address_list = user.addresses
    return render_template('address.html', address_list=address_list, address_default=address_default_id)

@mall.route('/select_address')
@login_required
def select_address():
    user = current_user._get_current_object()
    id = user.id
    address_list = user.addresses
    return render_template('select_address.html', address_list=address_list)

@mall.route('/edit_address', methods=['GET', 'POST'])
@login_required
def edit_address():
    user = current_user._get_current_object()
    if user == None:
        abort(404)  
    
    province_select = u''
    city_select = u''
    district_select = u''
    
    id = request.args.get('id', -1, type=int)
    if id!=-1:
        address = Address.query.get_or_404(id)
        province_select = address.province
        city_select = address.city
        district_select = address.district
    else:
        address = Address()
        address.user_id = user.id
    province_select = request.args.get('province', province_select)
    city_select = request.args.get('city', city_select)
    district_select = request.args.get('district', district_select)
    form = AddressForm(
        province = province_select, 
        city = city_select, 
        district = district_select,
        street = address.street,
        reciplents = address.reciplents,
        zip_code = address.zip_code,
        phone_number = address.phone_number)
    province_choices = [(u'',u'')] + [ (p.name, p.name) for p in Province.query.all() ]
    form.province.choices =  province_choices
    
    province_in_form = Province.query.filter_by(name=province_select).first()
    if province_in_form:
        city_choices = [((u'',u''))] + [(c.name, c.name) for c in province_in_form.citys]
        form.city.choices = city_choices

    city_in_form = City.query.filter_by(name=city_select).first()
    if city_in_form:
        district_choices = [(u'', u'')] + [ (d.name, d.name) for d in city_in_form.districts ]
        form.district.choices = district_choices
        
    if form.validate_on_submit():        
        address.province = form.province.data
        address.city = form.city.data
        address.district = form.district.data
        address.street = form.street.data
        address.reciplents = form.reciplents.data
        address.zip_code = form.zip_code.data
        address.phone_number = form.phone_number.data
        print address.province
        db.session.add(address)
        return redirect(request.args.get('next') or url_for('mall.address'))

    return render_template('edit_address.html', form=form)

@mall.route('/default_address')
@login_required
def default_address():
    user = current_user._get_current_object()
    address_id = request.args.get('id', -1, type=int)
    if address_id!=-1 and Address.query.get(address_id) in user.addresses:
        user.address_default_id = address_id

    return redirect(url_for('mall.address'))

@mall.route('/delete_address/<int:id>')
@login_required
def delete_address(id):
    user = current_user._get_current_object()
    address = Address.query.get(id)
    if address in user.addresses:
        if user.address_default_id==address.id:
            user.address_default_id = -1
        db.session.delete(address)
    return redirect(url_for('mall.address'))

@mall.route('/add_order', methods=['GET', 'POST'])
@login_required
def add_order():
    print request.method
    if request.method=='POST':
        deliver_date_info = request.form['deliver_date'].split('-')
        deliver_time = request.form['deliver_time']
        address_id = request.form['address']
        comment = request.form['comment']
        print deliver_time
        print address_id
        print comment
 
        cart_cookie = request.cookies.get('shopping_cart', None)
        total_sum = 0
        address = Address.query.get_or_404(address_id)
        new_order = greena_lib.create_order()

        user = current_user._get_current_object()
        new_order.user_id = user.id
        db.session.add(new_order)
        new_order.deliver_date = datetime.date(int(deliver_date_info[0]),int(deliver_date_info[1]),int(deliver_date_info[2]))
        new_order.deliver_time = deliver_time
        new_order.order_datetime = datetime.datetime.now() 
        new_order.comment = comment
        new_order.province = address.province
        new_order.city = address.city
        new_order.district = address.district
        new_order.street = address.street
        new_order.zip_code = address.zip_code
        new_order.reciplents = address.reciplents
        new_order.phone_number = address.phone_number
        db.session.add(new_order)

        if cart_cookie:
            cart_cookie = urllib.unquote(cart_cookie)
            shopping_cart = json.loads(cart_cookie)
            for cart_row in shopping_cart:
                product = Product.query.get_or_404(cart_row['id'])
                order_product = OrderProduct()
                order_product.order_id = new_order.order_id
                order_product.product_id = product.id
                order_product.count = cart_row['count']
                total_sum += product.price * cart_row['count']

                db.session.add(order_product)

            new_order.total_sum = total_sum

        return redirect(url_for('mall.order_info', id=new_order.id))
    else:
        return redirect(url_for('mall.mall'))

@mall.route('/orders')
@login_required
def orders():
    user = current_user._get_current_object()
    orders = user.orders
    return render_template('orders.html', orders=orders)

@mall.route('/order_info/<int:id>')
@login_required
def order_info(id):
    order = Order.query.get_or_404(id)
    return render_template('order_info.html', order=order)

@mall.route('/home')
def home():
    return render_template('home.html')

@mall.route('/mall/<string:product_type>')
def mall(product_type):
    product_type = ProductType.query.filter_by(name=product_type).first_or_404()
    products = product_type.products
    return render_template('mall.html', products=products)

