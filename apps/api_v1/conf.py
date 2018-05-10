# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from apps import db
from apps.models import ServerInfo, ServerThreshold, User
from apps.utils.record_log import record_operation_log
from . import api

"""分配服务器给用户"""


@api.route('/server', methods=['PUT'])
@login_required
def distribute_server():
    if current_user.authority == '0':
        return jsonify({'warning': '无权分配'})
    dict_ = request.get_json()
    s_id = dict_.get('s_id')
    try:
        server = ServerInfo.query.filter_by(id=s_id).first()
        server.user_id = dict_.get('u_id') if dict_.get('u_id') != '-1' else None
        db.session.commit()
        record_operation_log(operation=u'分配服务器:' + str(s_id), module=u'配置', result=u'成功', user_id=current_user.id)
    except Exception as e:
        db.session.rollback()
        record_operation_log(operation=u'分配服务器:' + str(s_id), module=u'配置', result=u'失败', user_id=current_user.id)
        return jsonify({'error': '分配失败'})
    return jsonify({'success': '分配成功'})


# 加载表格
@api.route('/server/table', methods=['GET'])
@login_required
def config_server_get_table():
    # /users/test?rows=10&page=1&sortOrder=asc&_=1524462815296
    row_list = []
    rows = request.args.get('rows', 10)
    page = request.args.get('page', 0)
    # 权限不同查询不同，用户只能查询自己分配到的服务器和还未分配的服务器
    user_id = current_user.id
    serverinfo = ServerInfo.query \
        .filter(or_(ServerInfo.user_id == user_id if not int(current_user.authority) else True, ServerInfo.user_id.is_(None))) \
        .order_by(ServerInfo.id.asc())
    servers = serverinfo.paginate(int(page), int(rows), False)
    counter_ = serverinfo.count()

    for server in servers.items:
        row_list.append({
            'id': server.id,
            'name': server.name,
            'ip': server.server_ip,
            'port': server.server_port,
            'os': server.server_os,
            'desc': server.server_desc,
            'ssh_name': server.ssh_name,
            'ssh_password': server.ssh_password,
            'u_id': server.user_id,
            'u_name': server.users.name if server.users else "",
        })
    return jsonify({'total': counter_, 'rows': row_list})


"""分配用户:获取用户列表"""


@api.route('/users/list', methods=['GET'])
@login_required
def get_all_users():
    users = User.query.all()
    user_dict = dict()
    for user in users:
        user_dict[user.id] = user.name
    return jsonify(user_dict)


"""获取告警配置table数据"""


@api.route('/alert/table', methods=['GET', 'PUT'])
@login_required
def alert_get_table():
    if request.method == 'GET':
        # /users/test?rows=10&page=1&sortOrder=asc&_=1524462815296

        row_list = []
        rows = request.args.get('rows', 10)
        page = request.args.get('page', 0)
        user_id = current_user.id if str(current_user.authority) == '0' else True
        # 做限制查询，对应用户的所有服务器配置
        if current_user.authority == '0':  # 普通用户
            servers_t = db.session.query(ServerThreshold).join(ServerInfo, User).filter(
                ServerThreshold.server_id == ServerInfo.id, ServerInfo.user_id == user_id) \
                .order_by(ServerThreshold.id.asc())
        else:  # 管理员
            servers_t = ServerThreshold.query.order_by(ServerThreshold.id.asc())

        counter_ = servers_t.count()
        servers_ = servers_t.paginate(int(page), int(rows), False)
        for server_th in servers_.items:
            dict_ = server_th.to_dict()
            if dict_.get('s_id'):
                server_info = ServerInfo.query.filter_by(id=dict_.get('s_id')).first()
                dict_['s_name'] = server_info.name
                dict_['ip'] = server_info.server_ip
                dict_['state'] = server_info.state
            row_list.append(dict_)
        return jsonify({'total': counter_, 'rows': row_list})
    # 更新告警配置
    if request.method == 'PUT':
        data = request.get_json()
        server = ServerThreshold.query.filter_by(id=data.get('id')).first()
        try:
            if len(data) > 2:
                server.server_cpu_th = data.get('s_cpu_th')
                server.server_mem_th = data.get('s_mem_th')
                server.server_disk_th = data.get('s_disk_th')
            server.servers.state = data.get('state')
            db.session.commit()
            record_operation_log(operation=u'更新告警:' + str(server.servers.id), module=u'配置', result=u'成功',
                                 user_id=current_user.id)
        except Exception as e:
            db.session.rollback()
            record_operation_log(operation=u'更新告警', module=u'配置', result=u'失败', user_id=current_user.id)
            return jsonify({'error': '更改失败！'})
        return jsonify({'success': '更改成功!'})


"""删除告警配置(共用服务器删除接口)"""
# @api.route('/alert/table', methods=['DELETE'])
# @login_required
# def alert_del_table():
#     arr = request.get_json().values()
#     print(list(arr))
#     return 'ok'
