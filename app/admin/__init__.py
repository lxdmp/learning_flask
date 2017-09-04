from flask import Blueprint

admin= Blueprint(
	'admin', 
	__name__, 
	template_folder='../templates/admin', 
	url_prefix='/admin')

from . import views, errors
