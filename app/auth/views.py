#encoding:utf-8
from flask import request, make_response, redirect, url_for
from flask.ext.login import login_user
from ..models import User, Role
from .. import db
from . import auth
from .. import greena_lib

@auth.route('/login')
def login():
    open_id = greena_lib.get_openid()
    user = User.query.filter_by(open_id=open_id).first()
    if user is not None:
        login_user(user)
        return redirect(request.args.get('next') or url_for('mall.mall'))
    else:
        user = User(open_id=open_id)
        role = Role.query.filter_by(name=u'微信用户').first()
        user.role = role
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(request.args.get('next') or url_for('mall.mall'))

