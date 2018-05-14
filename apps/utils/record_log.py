# -*- coding: utf-8 -*-
from flask_login import current_user
from .. import db
from ..models import OperationLog, AlertLog


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
    db.session.commit()


def record_alert_log(_threshold, _recording, _type, _desc, server_id):
    """记录告警日志"""
    result = {
        'threshold': _threshold,
        'recording': _recording,
        'type': _type,
        'desc': _desc,
        'server_id': server_id
    }
    # print(user_id)
    # OperationLog.user_id = user_id
    db.session.add(AlertLog(**result))
    db.session.commit()
