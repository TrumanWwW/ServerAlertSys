# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_login import login_required, current_user

from apps.models import User
from . import api

"""用户管理:加载表格"""


@api.route('/users/table', methods=['GET'])
@login_required
def users_get_table():
    # /users/test?rows=10&page=1&sortOrder=asc&_=1524462815296
    row_list = []
    rows = request.args.get('rows', 10)
    page = request.args.get('page', 0)
    users = User.query.filter(User.authority <= current_user.authority).order_by(User.id.asc()).paginate(int(page), int(rows), False)
    _dict = {'0': '用户', '1': '管理员', '2': '超级管理员'}
    for user in users.items:
        row_list.append({
            'id': user.id,
            'name': user.name,
            'auth': _dict.get(user.authority),
            'create_time': user.create_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({'total': User.query.count(), 'rows': row_list})
