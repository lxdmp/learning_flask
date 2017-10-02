from flask import Blueprint

stock_api = Blueprint(
	'stock_api', 
	__name__, 
	url_prefix='/stock_api')

from . import views, errors
