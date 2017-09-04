# coding=utf-8
import flask
import datetime
#from sqlalchemy import desc
from . import admin
#from .. import models
from forms import LoginForm

'''
@admin.route('/')
#@admin.route('/<string:user_name>')
def index():
	#flask.abort(404)
	return flask.render_template(
		"admin_index.html", 
		title = 'Admin', 
		current_time=datetime.datetime.utcnow())
'''

@admin.route('/', methods=['GET', 'POST'])
def login():
	name = None
	pw = None
	form = LoginForm()
	if form.validate_on_submit():
		name = form.user.data
		pw = form.pw.data
		form.user.data = ''
		form.pw.data = ''
		return flask.render_template(
			"admin_index.html", 
			title = '欢迎登录,%s'%(name), 
			name = name, 
			current_time=datetime.datetime.utcnow())
	else:
		return flask.render_template(
			"admin_login.html", 
			title = '登录', 
			form = form, 
			current_time=datetime.datetime.utcnow())

