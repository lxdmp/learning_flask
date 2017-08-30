# coding=utf-8
import flask
import flask_sqlalchemy
import flask_bootstrap
import flask_moment

'''
脚本/模版统一utf-8编码.
'''
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = flask.Flask(__name__) # 应用对象
app.config.from_object('config') # 配置
db = flask_sqlalchemy.SQLAlchemy(app) # ORM

bootstrap = flask_bootstrap.Bootstrap(app) # bootstrap
moment = flask_moment.Moment(app) # moment

from app import views,models
