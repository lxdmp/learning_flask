# coding=utf-8
import flask
import flask_sqlalchemy
import flask_bootstrap
import flask_moment
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

def create_app(config_name):
	app = flask.Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)

	# 自定义模板过滤
	from common import custom_filter_datetime
	app.jinja_env.filters['datetime'] = custom_filter_datetime

	# 蓝本注册
	from .blog import blog as blog_blueprint
	app.register_blueprint(blog_blueprint)

	# 首页重定向
	@app.route('/')
	def index():
		return flask.redirect(flask.url_for('blog.index'))
	
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
	
	return app

