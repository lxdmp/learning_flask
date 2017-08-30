# coding=utf-8
import flask
from app import app

import random
def random_int(start, end):
	return int(round(random.uniform(start, end)))

def random_content():
	len = random_int(10, 20)
	content = ''
	for i in range(len):
		num = random_int(0, 25)
		content = content + chr(ord('a')+num)
	return content

import datetime
@app.route('/')
@app.route('/index')
def index():
	user = {'nickname' : '铁剑震天南'}
	
	posts_num = 30
	posts = []
	for i in range(posts_num):
		new_item = {}
		new_item['author'] = {'nickname':random_content()}
		new_item['content'] = random_content()
		posts.append(new_item)
	'''
	posts = [
		{
			'author' : {'nickname' : '铁剑震天南'}, 
			'content' : random_content()
		}, 
		{
			'author' : {'nickname' : '匿名'}, 
			'content' : random_content()
		}, 
	]
	'''
	
	return flask.render_template(
		"index.html", 
		title = 'Home', 
		current_time=datetime.datetime.utcnow(), 
		user = user, 
		posts = posts)

