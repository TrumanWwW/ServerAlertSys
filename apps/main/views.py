# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request, flash, redirect
from flask_login import login_required, current_user

from apps import db
from apps.main.forms import AddUserForm, EditUserForm, AddServerForm
from apps.models import User, ServerInfo, ServerThreshold
from apps.utils.commons import auth_required
from apps.utils.record_log import record_operation_log
from . import main

"""首页视图"""


@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('dashboard/dashboard.html')


"""用户管理"""


# TODO:权限区分、密码重置

# 添加用户,修改用户
@main.route('/users', methods=['GET', 'POST', 'DELETE'])
@main.route('/users/edit', methods=['POST'])
@login_required
def users():
    form1 = AddUserForm(prefix="form1")
    form2 = EditUserForm(prefix="form2")
    # 添加用户
    if request.method == 'POST' and request.path == '/users':
        # 验证
        if not form1.validate_on_submit():
            flash({'error': form1.errors})
            return redirect(request.url)
        username = form1.username.data  # 账号名
        select = form1.select.data  # 所选权限
        user = User(name=username, authority=select)
        # 设置密码
        user.password = form1.password2.data
        # 尝试添加到数据库
        try:
            db.session.add(user)
            db.session.commit()
            # ‘success’、‘info’、‘warning’、‘error’
            flash({'success': u'添加成功!'})
            record_operation_log(operation=u'添加用户:' + str(user.id), module=u'用户', result=u'成功', user_id=current_user.id)
        except Exception as e:
            flash({'error': u'添加用户失败'})
            db.session.rollback()
            record_operation_log(operation=u'添加用户:' + username, module=u'用户', result=u'失败', user_id=current_user.id)
    # 修改用户
    if request.method == 'POST' and request.path == '/users/edit':
        # 验证
        if not form2.validate_on_submit():
            flash({'error': form2.errors})
            return redirect('/users')
        user_id = form2.user_id.data  # u_id
        user = User.query.filter_by(id=user_id).first()
        try:
            user.name = form2.username.data  # 账号名
            user.authority = form2.select.data  # 所选权限
            db.session.flush()
            flash({'success': u'修改成功!'})
            record_operation_log(operation=u'修改用户:' + str(user_id), module=u'用户', result=u'成功', user_id=current_user.id)
        except Exception as e:
            db.session.rollback()
            flash({'error': u'操作数据库失败，请检查用户名!'})
            record_operation_log(operation=u'修改用户:' + str(user_id), module=u'用户', result=u'失败', user_id=current_user.id)
    # 删除用户
    if request.method == 'DELETE':
        id_list = request.get_json().get('data')
        print(id_list)
        if len(id_list) == 0:
            print('-------------------')
            return jsonify({'warning': u'未选择!'})
        try:
            for id_ in id_list:
                db.session.delete(User.query.filter_by(id=id_).first())
                db.session.commit()
                record_operation_log(operation=u'删除用户:' + id_, module=u'用户', result=u'成功', user_id=current_user.id)
            return jsonify({'success': u'删除成功!'})
        except Exception as e:
            db.session.rollback()
            record_operation_log(operation=u'删除用户:' + str(id_list), module=u'用户', result=u'失败', user_id=current_user.id)
            return jsonify({'error': u'删除失败！'})

    return render_template('users/users.html', form1=form1, form2=form2)


"""配置管理"""


@main.route('/config', methods=['GET', 'POST'])
@main.route('/config/server', methods=['GET', 'POST', 'DELETE'])
@login_required
def config_server():
    form1 = AddServerForm(prefix="form1")
    if request.method == 'POST':
        # 验证
        if not form1.validate_on_submit():
            flash({'error': form1.errors})
            return redirect(request.url)
        dict_ = {'name': form1.name.data,  # 账号名
                 'server_ip': form1.ip.data,  # 所选权限
                 'server_port': form1.port.data,  # 端口
                 'server_os': form1.os.data,  # 系统
                 'ssh_name': form1.ssh_u.data,  # 账户
                 'ssh_password': form1.ssh_p.data,  # 密码
                 'server_desc': form1.desc.data  # 备注
                 }
        # 更新
        if request.form.to_dict().get('s_id'):
            server = ServerInfo.query.filter_by(id=request.form.to_dict().get('s_id')).first()
            for k, v in dict_.items():
                setattr(server, k, v)
            db.session.commit()
            flash({'success': u'更新服务器成功!'})
            record_operation_log(operation=u'修改服务器', module=u'配置', result=u'成功', user_id=current_user.id)
        # 添加
        else:

            server = ServerInfo(**dict_)
            # 尝试添加到数据库
            try:
                db.session.add(server)
                db.session.flush()
                db.session.add(ServerThreshold(server_id=server.id))
                db.session.commit()
                # ‘success’、‘info’、‘warning’、‘error’
                flash({'success': u'添加服务器成功!'})
                record_operation_log(operation=u'添加服务器:' + str(server.id), module=u'配置', result=u'成功',
                                     user_id=current_user.id)
            except Exception as e:
                flash({'error': u'添加服务器失败'})
                db.session.rollback()
                record_operation_log(operation=u'添加服务器', module=u'配置', result=u'失败', user_id=current_user.id)
    if request.method == 'DELETE':
        id_list = request.get_json().get('data')
        if len(id_list) == 0:
            print('-------------------')
            return jsonify({'warning': u'未选择!'})
        try:
            for id_ in id_list:
                db.session.delete(ServerInfo.query.filter_by(id=id_).first())
                db.session.commit()
            record_operation_log(operation=u'删除服务器:' + str(id_list)[2:-2], module=u'配置', result=u'成功',
                                 user_id=current_user.id)
            return jsonify({'success': u'删除成功!'})
        except Exception as e:
            db.session.rollback()
            record_operation_log(operation=u'删除服务器:' + str(id_list)[2:-2], module=u'配置', result=u'失败',
                                 user_id=current_user.id)
            return jsonify({'error': u'删除失败！'})
    return render_template('config/server.html', form1=form1)


@main.route('/config/alert', methods=['GET', 'POST'])
@login_required
def config_alert():
    return render_template('config/alert.html')


"""日志LOG"""


@main.route('/log/operation', methods=['GET'])
@login_required
def render_operation_log():
    return render_template('log/operation.html')


@main.route('/log/alert', methods=['GET'])
@login_required
def render_alert_log():
    return render_template('log/alert.html')
