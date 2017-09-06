# coding=utf-8

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

def custom_filter_datetime(s):
	'''
	对模板中的datetime类型过滤输出
	'''
	from datetime import datetime
	if type(s)==datetime:
		from re import match
		pattern = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
		result = match(pattern, str(s))
		if result:
			return result.string[result.start() : result.end()]
		else:
			return s
	else:
		 return s
	
def url_for_bp(bp, url):
	'''
	格式化某个蓝图中的视图url
	'''
	from flask import url_for
	return url_for('.'.join((bp.name, url)))

