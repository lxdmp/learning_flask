# coding=utf-8
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	name = db.Column(db.String(32), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User %r>'%(self.name)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement = True)
	body = db.Column(db.String(1024))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post %r>'%(self.body)

