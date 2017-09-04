# coding=utf-8
import flask
import datetime
#from sqlalchemy import desc
from . import admin
#from .. import models

@admin.route('/')
#@admin.route('/<string:user_name>')
def index():
	flask.abort(404)
	return flask.render_template(
		"admin_index.html", 
		title = 'Admin', 
		current_time=datetime.datetime.utcnow())
