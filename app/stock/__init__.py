from flask import Blueprint

stock = Blueprint(
	'stock', 
	__name__, 
	template_folder='../templates/stock', 
	url_prefix='/stock')

from . import views, errors

