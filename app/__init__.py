# coding=utf-8
import flask
import flask_sqlalchemy
import flask_bootstrap
import flask_moment
import flask_socketio
import flask_apscheduler
from config import config

'''
脚本/模版统一utf-8编码.
'''
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

db = flask_sqlalchemy.SQLAlchemy() # ORM
bootstrap = flask_bootstrap.Bootstrap() # bootstrap
moment = flask_moment.Moment() # moment
socketio = flask_socketio.SocketIO() # socket io
scheduler = flask_apscheduler.APScheduler() # scheduelr

def sin_data_gen():
	pass

class AppWrapper(object):

	def __init__(self, app):
		self._app = app
	
	def run(self):
		assert(self._app!=None)
		if not scheduler.running:
			scheduler.start()
		socketio.run(self._app)

def create_app(config_name):
	app = flask.Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	socketio.init_app(app)
	scheduler.init_app(app)

	# 自定义模板过滤
	from common import custom_filter_datetime
	app.jinja_env.filters['datetime'] = custom_filter_datetime

	# 蓝本注册
	from .blog import blog as blog_bp
	app.register_blueprint(blog_bp)

	from .admin import admin as admin_bp
	app.register_blueprint(admin_bp)

	from .common import url_for_bp
	# 首页重定向
	@app.route('/')
	def index():
		return flask.redirect(url_for_bp(blog_bp, 'index'))

	# 错误重定向
	@app.errorhandler(404)
	def page_not_found(error):
		return flask.render_template(
			"page_not_found.html", 
			target_url=url_for_bp(blog_bp, 'index'), 
			delay_sec=4), 404
	
	@app.errorhandler(500)
	def internal_error(error):
		return flask.render_template("internal_error.html"), 500
	
	# 请求预处理(若访问蓝图,将蓝图的路径设为优先搜索路径)
	'''
	@app.before_request
	def before_request_hook():
		from flask import request
		print app.jinja_loader.searchpath
		if request.blueprint is not None:
			bp = app.blueprints[request.blueprint]
			if bp.jinja_loader is not None:
				new_path = list(set(bp.jinja_loader.searchpath).union(set(app.jinja_loader.searchpath)))
				app.jinja_loader.searchpath = new_path
	'''
	return AppWrapper(app)

