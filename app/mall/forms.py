#encoding: utf-8

from flask.ext.wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, Regexp

class AddressForm(Form):
    province = SelectField(u'省/直辖市', 
        choices= [],
        validators=[Required(), Length(1,64)])
    #province = StringField(u'省/直辖市', validators=[Required(), Length(1,64)])
    city = SelectField(u'城市', choices=[], validators=[Required(), Length(1, 64)])
    #city = StringField(u'城市', validators=[Required(), Length(1,64)])
    district = SelectField(u'区', choices=[], validators=[Required(), Length(1, 64)])
    #district = StringField(u'区', validators=[Required(), Length(1,64)])
    street = TextAreaField(u'详细地址', validators=[Required(), Length(1,64)])
    zip_code = StringField(u'邮政编码', validators=[
        Required(), 
        Length(1,64), 
        Regexp('^[0-9]{6}$', 0, u'请输入六位数字')])
    reciplents = StringField(u'收货人', validators=[Required(), Length(1,64)])
    phone_number = StringField(u'手机/电话号码', validators=[
        Required(), 
        Length(1,64),
        Regexp('^[0-9]{5,13}$', 0, u'请输入5至13位数字')])
    submit = SubmitField(u'提交')

