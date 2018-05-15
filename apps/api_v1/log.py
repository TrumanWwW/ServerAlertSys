# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import and_

from apps import db
from apps.models import OperationLog, AlertLog, ServerInfo, User
from . import api


@api.route('/log/operation/table', methods=['GET'])
@login_required
def log_operation_get_table():
    if request.method == 'GET':
        # /users/test?rows=10&page=1&sortOrder=asc&_=1524462815296
        rows = request.args.get('rows', 10)
        page = request.args.get('page', 0)
        sortOrder = request.args.get('sortOrder', 'desc')
        sort = request.args.get('sort', 'id')
        type = request.args.get('type') or False
        user_id = current_user.id
        logs = OperationLog.query \
            .filter(and_(OperationLog.module == type,
                         OperationLog.user_id == user_id if current_user.authority == '0' else True)) \
            .order_by(sort + ' ' + sortOrder)
        row_list = []
        for log_ in logs.paginate(int(page), int(rows), False).items:
            dict_ = log_.to_dict()
            dict_['u_name'] = log_.users.name if log_.users else None
            row_list.append(dict_)
        return jsonify({'total': logs.count(), 'rows': row_list})


@api.route('/log/alert/table', methods=['GET', 'PUT'])
@login_required
def log_alert_get_table():
    if request.method == 'GET':
        # /users/test?rows=10&page=1&sortOrder=asc&_=1524462815296
        row_list = []
        rows = request.args.get('rows', 10)
        page = request.args.get('page', 0)
        sortOrder = request.args.get('sortOrder', 'desc')
        sort = request.args.get('sort', 'id')
        type_ = request.args.get('type') or False

        # 用户：用户分配到的所有服务器的所有告警，管理员:所有告警
        # logs = AlertLog.query.filter_by(type=type).order_by(sort + ' ' + sortOrder)
        logs = db.session.query(AlertLog) \
            .join(ServerInfo, User) \
            .filter(AlertLog.type == type_,
                    AlertLog.server_id == ServerInfo.id,
                    ServerInfo.user_id == current_user.id if current_user.authority == '0' else True) \
            .order_by('alert_log.' + sort + ' ' + sortOrder)

        for log_ in logs.paginate(int(page), int(rows), False).items:
            dict_ = log_.to_dict()
            dict_['s_name'] = log_.servers.name if log_.servers else None
            row_list.append(dict_)
        return jsonify({'total': logs.count(), 'rows': row_list})
