# coding=utf-8
import flask
from . import blog

@blog.app_errorhandler(404)
def page_not_found(error):
	return flask.render_template(
		"page_not_found.html", 
		target_url=flask.url_for('blog.index'), 
		delay_sec=3), 404

@blog.app_errorhandler(500)
def internal_error(error):
	return flask.render_template("internal_error.html"), 500

