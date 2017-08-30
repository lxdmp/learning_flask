# coding=utf-8

# 应用路径
import os
basedir = os.path.abspath(os.path.dirname(__file__)) 

# Flask-WTF(web表单配置)
CSRF_ENABLED = True # 使能"跨站点请求伪造"保护
SECRET_KEY = 'lxdmp' # 设置加密密匙

# db配置(使用sqlite)
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# flask-bootstrap配置
BOOTSTRAP_SERVE_LOCAL = True # 使用本地的css/js文件

