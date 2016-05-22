#coding:utf-8
from flask import render_template,request, url_for, redirect
from flask.ext.login import login_required, current_user
from . import mall
from .. import db
from ..models import Product, Address, Province, City, District
from forms import AddressForm
import json
import urllib

@mall.route('/product/<int:id>')
@login_required
def product(id):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)

@mall.route('/shopping_cart')
@login_required
def shopping_cart():
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

    return render_template('shopping_cart.html', products=products, empty_cart=empty_cart, total_sum=total_sum)

@mall.route('/user')
@login_required
def user_center():
    return render_template('user_center.html', user=current_user)

@mall.route('/address')
@login_required
def address():
    id = current_user.id
    address_list = Address.query.filter_by(user_id=id).all()
    return render_template('address.html', address_list=address_list)

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
        return redirect(url_for('mall.address'))

    return render_template('edit_address.html', form=form)

@mall.route('/mall', methods=['GET', 'POST'])
def mall():
    products = Product.query.all()
    return render_template('mall.html', products=products)
