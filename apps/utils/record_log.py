# -*- coding: utf-8 -*-
from flask_login import current_user
from .. import db
from ..models import OperationLog


# 记录操作日志

def record_operation_log(operation, module, user_id='', result=u'成功'):
    """记录操作日志"""
    if 'id' in dir(current_user):
        user_id = current_user.id
    else:
        user_id = user_id
    result = {
        'operation': operation,
        'operation_res': result,
        'user_id': user_id,
        'module': module
    }
    # print(user_id)
    # OperationLog.user_id = user_id
    db.session.add(OperationLog(**result))
