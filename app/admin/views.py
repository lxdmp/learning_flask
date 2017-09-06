# coding=utf-8
import flask
import datetime
#from sqlalchemy import desc
from . import admin
#from .. import models
from forms import LoginForm
from ..common import url_for_bp

@admin.route('/')
def index():
	#flask.abort(404)
	name = flask.session.get('name')
	if not name:
		return flask.redirect(url_for_bp(admin, 'login'))
	else:
		return flask.render_template(
			"admin_index.html", 
			title = '欢迎登录,%s'%(name), 
			name = name, 
			current_time=datetime.datetime.utcnow())

@admin.route('/login', methods=['GET', 'POST'])
def login():
	if flask.session.get('name'):
		return flask.redirect(url_for_bp(admin, 'index'))

	form = LoginForm()
	if form.validate_on_submit():
		name = form.user.data
		pw = form.pw.data
		form.user.data = ''
		form.pw.data = ''
		flask.session['name'] = name
		return flask.redirect(url_for_bp(admin, 'index'))
	else:
		return flask.render_template(
			"admin_login.html", 
			title = '登录', 
			form = form, 
			current_time=datetime.datetime.utcnow())

