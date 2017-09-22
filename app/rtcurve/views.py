# coding=utf-8
import flask
import datetime
from . import rtcurve
import threading
from .. import socketio

@socketio.on('connect')
def test_connect():
	pass

@socketio.on('disconnect')
def test_disconnect():
	pass

custom_data_lock = threading.Lock()
def sin_data_gen():
	import random
	with custom_data_lock:
		val = random.random()*16+4
		socketio.emit('msg', {'data': val})

rtcurve._before_request_lock = threading.Lock()
rtcurve._first_req_got = False
@rtcurve.before_request
def init_rtcurve_bp():
	if rtcurve._first_req_got:
		return
	with rtcurve._before_request_lock:
		if rtcurve._first_req_got:
			return
		rtcurve._first_req_got = True

		# 蓝图初次执行需做的初始化
		from .. import scheduler
		scheduler.add_job(
			id='sin_data',
			func=sin_data_gen, 
			args=None, 
			trigger='interval', 
			seconds=1
		)

@rtcurve.route('/')
def index():
	return flask.render_template(
		"rtcurve_index.html")

