#! flask/bin/python
# coding=utf-8
import sys
from app import db, models

def do_add():
	user = [
		{'name':'铁剑震天南', 'email':'yudmp@sina.com'}, 
		{'name':'匿名1', 'email':'xxx@126.com'},
	]

	reload(sys)
	sys.setdefaultencoding("utf-8")

	for	i in range(len(user)):
		u = models.User(name=unicode(user[i]['name']), email=user[i]['email'])
		db.session.add(u)
	db.session.commit()

def do_query():
	users = models.User.query.all()
	for u in users:
		print u.id, u.name, u.email

def do_post():
	import datetime
	u = models.User.query.get(1)
	p = models.Post(body='post content!', timestamp=datetime.datetime.now(), author = u)
	db.session.add(p)
	db.session.commit()

if __name__=='__main__':
	'''
	测试Flask的ORM
	'''
	#do_add()
	do_query()
	#do_post()

