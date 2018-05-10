# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, IPAddress


class AddUserForm(FlaskForm):
    username = StringField(u'用户名',
                           validators=[DataRequired(message=u'用户名不为空'), Length(1, 12, message=u'用户名的长度在1到12之间')])
    select = SelectField(u'authority', choices=[('0', '用户'), ('1', '管理员'), ('2', '超级管理员'), ])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码不为空')])
    password2 = PasswordField(u'密码', validators=[DataRequired(message=u'密码不为空'), EqualTo('password', message=u'密码不一致')])
    submit = SubmitField(u'提交')


class EditUserForm(FlaskForm):
    user_id = IntegerField()
    username = StringField(u'用户名',
                           validators=[DataRequired(message=u'用户名不为空'), Length(1, 12, message=u'用户名的长度在1到12之间')])
    select = SelectField(u'authority', choices=[('0', '用户'), ('1', '管理员'), ('2', '超级管理员'), ])
    submit = SubmitField(u'提交')


class AddServerForm(FlaskForm):
    name = StringField(u'服务器名',
                       validators=[DataRequired(message=u'服务器名不为空'), Length(1, 12, message=u'服务器名的长度在1到12之间')])
    ip = StringField(u'服务器ip地址',
                     validators=[DataRequired(message=u'服务器ip地址不为空'), Length(7, 15, message=u'服务器ip地址的长度在7到15之间'),
                                 IPAddress(message=u'服务器ip地址不正确')])
    port = IntegerField(u'端口号',
                        validators=[DataRequired(message=u'端口号不为空'),
                                    NumberRange(min=0, max=65535, message=u'端口号范围0~65535')])
    os = StringField(u'操作系统(选填)')
    ssh_u = StringField(u'SSH账户',
                        validators=[DataRequired(message=u'SSH账户不为空')])
    ssh_p = StringField(u'SSH密码',
                        validators=[DataRequired(message=u'SSH密码不为空')])
    desc = StringField(u'备注',
                       validators=[Length(1, 12, message=u'备注长度在1到128之间')])

    submit = SubmitField(u'提交')
