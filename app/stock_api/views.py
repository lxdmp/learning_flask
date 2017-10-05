# coding=utf-8
import flask
import datetime
import re
from . import stock_api
import mysql.connector

@stock_api.before_request
def stock_api_before_req():
	config = {
		'user' : flask.current_app.config.get('STOCK_DB_USER'), 
		'password' : flask.current_app.config.get('STOCK_DB_PW'), 
		'host' : flask.current_app.config.get('STOCK_DB_HOST'), 
		'database' : flask.current_app.config.get('STOCK_DB_NAME')
	}
	conn = mysql.connector.connect(**config)
	if conn:
		flask.g.stock_db = conn

@stock_api.after_request
def stock_api_after_req(response):
	if hasattr(flask.g, 'stock_db'):
		flask.g.stock_db.close()
	return response


def format_error_msg(msg_code, msg):
	if not isinstance(msg_code, int):
		msg_code = int(msg_code)
	if not isinstance(msg, str):
		msg = str(msg)
	return flask.make_response(flask.jsonify({'error': msg}), msg_code)

def format_day_row(row):
	row = list(row)
	row[0] = str(row[0])
	row[1] = row[1]/1000.0
	row[2] = row[2]/1000.0
	row[3] = row[3]/1000.0
	row[4] = row[4]/1000.0
	row[5] = row[5]/10.0
	row[6] = row[6]/1.0
	return row

# 查询一段范围内的行情
def query_range_day_info(id):
	conn = flask.g.stock_db
	start_date = flask.request.args.get('start')
	end_date = flask.request.args.get('end')
	date_pattern = '[\d]{8}'

	if not start_date:
		return None
	if not re.match(date_pattern, start_date):
		return None

	if not end_date:
		end_date = start_date
	if not re.match(date_pattern, end_date):
		return None

	id = int(id)
	start_year = int(start_date[:4])
	start_mon = int(start_date[4:6])
	start_day = int(start_date[6:8])
	end_year = int(end_date[:4])
	end_mon = int(end_date[4:6])
	end_day = int(end_date[6:8])

	start_date = datetime.datetime(start_year, start_mon, start_day, 0, 0, 0)
	end_date = datetime.datetime(end_year, end_mon, end_day, 0, 0, 0)
	if start_date>end_date:
		return None
	
	result = []
	cursor = conn.cursor()
	query = (
		"select date,open,close,high,low,amount,volume from Day where id=%06d and date>='%04d-%02d-%02d' and date<='%04d-%02d-%02d' order by date asc" % (id, start_year, start_mon, start_day, end_year, end_mon, end_day) )
	cursor.execute(query)
	for item in cursor:
		result.append(format_day_row(item))
	cursor.close()

	return flask.jsonify(result),200

# 查询指定时间点前的行情
def query_prev_day_info(id):
	conn = flask.g.stock_db
	is_prev = flask.request.args.get('prev')
	count = flask.request.args.get('count')
	date = flask.request.args.get('date')
	date_pattern = '[\d]{8}'

	if not is_prev or not count or not date:
		return None

	if not is_prev.lower()=='true':
		return None
	if not re.match(date_pattern, date):
		return None
	count = int(count)

	id = int(id)
	year = int(date[:4])
	mon = int(date[4:6])
	day = int(date[6:8])

	result = []
	cursor = conn.cursor()
	query = (
		"select date,open,close,high,low,amount,volume from Day where id=%06d and date<'%04d-%02d-%02d' order by date desc limit %d" % (id, year, mon, day, count) )
	cursor.execute(query)
	for item in cursor:
		result.append(format_day_row(item))
	cursor.close()

	return flask.jsonify(result),200

# 查询指定时间点后的行情
def query_next_day_info(id):
	conn = flask.g.stock_db
	is_next = flask.request.args.get('next')
	count = flask.request.args.get('count')
	date = flask.request.args.get('date')
	date_pattern = '[\d]{8}'

	if not is_next or not count or not date:
		return None

	if not is_next.lower()=='true':
		return None
	if not re.match(date_pattern, date):
		return None
	count = int(count)

	id = int(id)
	year = int(date[:4])
	mon = int(date[4:6])
	day = int(date[6:8])

	result = []
	cursor = conn.cursor()
	query = (
		"select date,open,close,high,low,amount,volume from Day where id=%06d and date>'%04d-%02d-%02d' order by date asc limit %d" % (id, year, mon, day, count) )
	cursor.execute(query)
	for item in cursor:
		result.append(format_day_row(item))
	cursor.close()

	return flask.jsonify(result),200

@stock_api.route('/day/<regex("\d{6}"):id>/')
def day(id):
	if not hasattr(flask.g, 'stock_db'):
		return format_error_msg(500, 'Can not connec to db server')
	conn = flask.g.stock_db
	
	tbl = [
		query_range_day_info, # ?start=yyyymmdd&end=yyyymmdd
		query_prev_day_info, # ?prev=true&date=yyyymmdd&count=xx
		query_next_day_info # ?next=true&date=yyyymmdd&count=xx
	]
	for i in range(len(tbl)):
		ret = tbl[i](id)
		if ret!=None:
			return ret
	return format_error_msg(404, 'Invalid request args')

