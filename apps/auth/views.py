# -*- coding: utf-8 -*-
"""登录登出模块"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from apps.utils.record_log import record_operation_log
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm
from .. import db


# 登录
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash({'errors': form.errors})
            return redirect(request.url)

        username = form.username.data
        user = User.query.filter_by(name=username).first()
        # 校验成功
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            record_operation_log(operation=u'登入', module=u'用户')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash({'errors': u'用户名或者密码错误'})
            record_operation_log(operation=u'登入', module=u'用户', result=u'失败', user_id=user.id)
            return redirect(request.url)

    return render_template('auth/login.html', form=form, title='登录', auth={'url': '/register', 'word': '去注册'})


# 注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # form = LoginForm()
    form = RegisterForm()
    if request.method == 'POST':
        # 前端验证
        # print(request.form.to_dict())
        if not form.validate_on_submit():
            flash({'errors': form.errors})
            return redirect(request.url)

        # 账号名
        username = form.username.data
        user = User(name=username, authority=0)
        # 设置密码
        user.password = form.password2.data
        # 尝试添加到数据库
        try:
            db.session.add(user)
            record_operation_log(operation=u'注册', module=u'用户', result=u'成功', user_id=user.id)
            flash({'errors': u'添加成功,请登录!'})
            return redirect(request.args.get('next') or url_for('auth.login'))
        except Exception as e:
            flash({'errors': u'添加用户失败'})
            record_operation_log(operation=u'注册', module=u'用户', result=u'失败', user_id=user.id)
            db.session.rollback()
            return redirect(request.url)

    return render_template('auth/login.html', form=form, title=u'注册', auth={'url': '/login', 'word': u'去登录'})


# 登出
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
