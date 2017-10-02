# coding=utf-8
import flask
import datetime
from . import stock

@stock.route('/')
def index():
	return flask.render_template(
		"stock_index.html")

