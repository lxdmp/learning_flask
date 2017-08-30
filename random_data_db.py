# coding=utf-8
from app import app
from app import views,models
from app import db
from app.common import random_content
from datetime import datetime

# 在库中插入随机数据
def insert_test():
	tbl = [
		{'name':'铁剑震天南', 'email':'yudmp@sina.com'}
	]
	for i in range(len(tbl)):
		try:
			u = models.User(name=unicode(tbl[i]['name']), email=tbl[i]['email'])
			db.session.add(u)
			db.session.commit()
		except:
			db.session.rollback()
			u = db.session.query(models.User).filter(models.User.name==unicode(tbl[i]['name'])).first()
			print 'duplicate User : %d %s %s' % (u.id, u.name, u.email)

	u = models.User.query.get(1)
	try:
		for i in range(100):
			new_item = models.Post(body=random_content(), timestamp=datetime.now(), author=u)
			db.session.add(u)
		db.session.commit()
	except Exception as e:
		print e

def clean_test():
	posts = models.Post.query.all()
	for post in posts:
		db.session.delete(post)
	db.session.commit()
	
	users = models.User.query.all()
	for user in users:
		db.session.delete(user)
	db.session.commit()

if __name__=='__main__':
	insert_test()
	#clean_test()

