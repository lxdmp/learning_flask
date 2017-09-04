# coding=utf-8
import flask
import datetime
from sqlalchemy import desc
from . import blog
from .. import models

@blog.route('/')
@blog.route('/<int:page>')
def index(page=1):
	if page<1:
		page = 1
	each_page = 15
	posts = models.Post.query.order_by(desc('timestamp')).paginate(page, per_page=each_page)
	return flask.render_template(
		"blog_index.html", 
		title = 'Blog', 
		current_time=datetime.datetime.utcnow(), 
		posts = posts)

