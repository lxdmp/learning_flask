from flask import Blueprint

blog = Blueprint(
	'blog', 
	__name__, 
	template_folder='../templates/blog', 
	url_prefix='/blog')

from . import views, errors
