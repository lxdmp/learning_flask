# coding=utf-8
import flask
from sqlalchemy import desc
from app import app
from app import models
import datetime

@app.errorhandler(404)
def page_not_found(error):
	return flask.render_template("page_not_found.html"), 404

@app.errorhandler(500)
def internal_error(error):
	return flask.render_template("internal_error.html"), 500

@app.route('/')
@app.route('/index/')
@app.route('/index/<int:page>')
def index(page=1):
	if page<1:
		page = 1
	each_page = 20
	#posts = models.Post.query.order_by(desc('timestamp')).offset((page-1)*each_page).limit(each_page).all()
	#posts = models.Post.query.order_by(desc('timestamp')).paginate(page, per_page=each_page, error_out = False)
	posts = models.Post.query.order_by(desc('timestamp')).paginate(page, per_page=each_page)
	return flask.render_template(
		"index.html", 
		title = 'Home', 
		current_time=datetime.datetime.utcnow(), 
		posts = posts)

