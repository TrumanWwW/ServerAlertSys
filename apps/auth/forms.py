# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(message=u'用户名不为空'), Length(1, 12, message='用户名的长度在1到12之间')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码不为空')])
    remember_me = BooleanField(u'记住我', default=False)
    submit = SubmitField(u'登录')


class RegisterForm(LoginForm):
    password2 = PasswordField(u'密码', validators=[DataRequired(message=u'密码不为空'), EqualTo('password', message='密码不一致')])
    remember_me = ''
    submit = SubmitField(u'注册')
