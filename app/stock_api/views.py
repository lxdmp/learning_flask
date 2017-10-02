# coding=utf-8
import flask
import datetime
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

@stock_api.route('/day/<regex("\d{6}"):id>/<regex("\d{8}"):start_date>')
@stock_api.route('/day/<regex("\d{6}"):id>/<regex("\d{8}"):start_date>-<regex("\d{8}"):end_date>')
def day(id, start_date, end_date=None):
	if not hasattr(flask.g, 'stock_db'):
		return format_error_msg(500, 'Can not connec to db server')
	conn = flask.g.stock_db

	if end_date==None:
		end_date = start_date

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
		return format_error_msg(404, 'Request date range error')
	
	result = []
	cursor = conn.cursor()
	query = (
		"select date,open,close,high,low,amount,volume from Day where id=%06d and date>='%04d-%02d-%02d' and date<='%04d-%02d-%02d' order by date asc" % (id, start_year, start_mon, start_day, end_year, end_mon, end_day) )
	cursor.execute(query)
	for item in cursor:
		result.append(format_day_row(item))
	cursor.close()

	return flask.jsonify(result),200
	'''
	return flask.jsonify({
		'id' : id, 
		'start' :'%04d-%02d-%02d'%(start_year, start_mon, start_day), 
		'end' : '%04d-%02d-%02d'%(end_year, end_mon, end_day) 
	}),200
	'''

