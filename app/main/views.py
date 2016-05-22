# -*- coding:utf8 -*-
from . import main
import time
from flask import Flask, request, make_response, url_for, redirect, json, jsonify
import hashlib

@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
#main.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

@main.route('/', methods=['GET', 'POST'])
def wechat_auth():
	if request.method == 'GET':
		token = '5dO4ULr2XqHbkxTzfIawm6ouBDR3zqJ6NAU7nQsWToxGjgLObhMkvm4V'	# your token
		query = request.args	# GET 方法附上的参数
		signature = query.get('signature', '')
		timestamp = query.get('timestamp', '')
		nonce = query.get('nonce', '')
		echostr = query.get('echostr', '')
		print echostr
		s = [timestamp, nonce, token]
		s.sort()
		s = ''.join(s)
		if ( hashlib.sha1(s).hexdigest() == signature ):
			return make_response(echostr)
	
	elif request.method == 'POST':
		pass


	return make_response('')

@main.route('/json')
def get_json():
    result = {'userid':12, 'openid':'xxxxxxxxxxxxxxx', 'other':False}
    return json.jsonify(result)
    
