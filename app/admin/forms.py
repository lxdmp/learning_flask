# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import Required

class LoginForm(FlaskForm):
	user = StringField('用户名', validators=[
		Required(message='该字段不能为空')
	])
	pw = PasswordField('密码', validators=[
		Required(message='该字段不能为空')
	])
	submit = SubmitField('提交')

