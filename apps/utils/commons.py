# -*- coding:utf-8 -*-
from flask_login import current_user
from werkzeug.routing import BaseConverter

from functools import wraps
from flask import session, jsonify, g, render_template


class RegexConverter(BaseConverter):
    """自定义正则转换器"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)


#         self.regex = args[0]

# def login_required(view_func):
#     """检验用户的登录状态"""
#
#     @wraps(view_func)
#     def wrapper(*args, **kwargs):
#
#         user_id = session.get("user_id")
#         if user_id is not None:
#             # 表示用户已经登录
#             # 使用g对象保存user_id，在视图函数中可以直接使用
#             # 比如后面设置头像的时候, 仍然需要获取session的数据. 为了避免多次访问redis服务器. 可以使用g变量
#             g.user_id = user_id
#             return view_func(*args, **kwargs)
#         else:
#             # 用户未登录
#             resp = {
#                 "msg": "用户未登录"
#             }
#             return jsonify(resp)
#
#     return wrapper


def auth_required(auth=2):
    """检验用户的权限"""

    def foo(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if int(current_user.authority) < auth:
                return render_template('403.html')
            return view_func(*args, **kwargs)

        return wrapper

    return foo
