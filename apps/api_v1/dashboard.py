# -*- coding: utf-8 -*-
import time
from flask import jsonify
from flask_login import current_user, login_required

from apps import db
from apps.api_v1 import api
from apps.models import ServerThreshold, ServerInfo, User, LatestServerInfo

"""首页仪表盘"""


@api.route('/dashboard/list', methods=['GET'])
@login_required
def get_dashboard_server_list():
    """服务器列表"""
    user_id = current_user.id if str(current_user.authority) == '0' else True
    # 当前用户分配到的服务器
    servers = db.session.query(ServerThreshold).join(ServerInfo, User).filter(
        ServerThreshold.server_id == ServerInfo.id, ServerInfo.user_id == user_id) \
        .order_by(ServerThreshold.id.asc()).all()

    _list = []
    for server in servers:
        state = server.servers.state
        latest_ser = LatestServerInfo.query.filter_by(server_id=server.servers.id).first()
        if latest_ser and state:
            state = 'highLoad' if latest_ser.cpu_rate != '--' and float(latest_ser.cpu_rate) > 50 else state
        _list.append({
            'state': state,
            'name': server.servers.name,
            's_id': server.servers.id,
            'ip': server.servers.server_ip,
        })

    return jsonify(_list)


@api.route('/dashboard/server/<string:s_id>', methods=['GET'])
@login_required
def get_dashboard_server_info(s_id):
    if s_id == 'undefined':
        return jsonify({'warning': '未设置监听或不存在该服务器!'})
    server = LatestServerInfo.query.filter_by(server_id=int(s_id)).first()
    info = server.to_dict() if server else dict()
    info['timeStamp'] = int(time.time() * 1000)  # 时间戳
    return jsonify(info)
