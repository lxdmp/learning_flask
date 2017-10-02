# coding=utf-8
import flask
from . import stock_api

@stock_api.errorhandler(404)
def api_not_found(error):
	return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

@stock_api.errorhandler(500)
def api_internal_error(error):
	return flask.make_response(flask.jsonify({'error': 'Internal error'}), 500)

