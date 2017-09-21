from flask import Blueprint

rtcurve = Blueprint(
	'rtcurve', 
	__name__, 
	template_folder='../templates/rtcurve', 
	url_prefix='/rtcurve')

from . import views, errors

