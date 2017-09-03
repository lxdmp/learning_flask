# coding=utf-8

# 应用路径
import os
_basedir = os.path.abspath(os.path.dirname(__file__)) 

# 基础配置
class Config(object):
	THREADED = True
	
	# Flask-WTF(web表单配置)
	CSRF_ENABLED = True # 使能"跨站点请求伪造"保护
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'lxdmp' # 设置加密密匙

	@staticmethod
	def init_app(app):
		pass

# 开发环境配置
class DevConfig(Config):
	DEBUG =True
	
	# db配置(使用sqlite)
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(_basedir, 'app.db')
	SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	
	# flask-bootstrap配置
	BOOTSTRAP_SERVE_LOCAL = True # 使用本地的css/js文件

config = {
	'dev' : DevConfig, 
	'default' : DevConfig
}

