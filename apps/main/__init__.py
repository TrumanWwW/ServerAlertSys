# -*- coding: utf-8 -*-
# 管理api的路由, 应该使用蓝图的目录方式去实现

from flask import Blueprint

# 创建蓝图对象Blueprint('蓝图名称','蓝图资源查找','蓝图url前缀')
# url_prefix是给蓝图下所有函数预先添加前缀
main = Blueprint('main', __name__, url_prefix='')

from . import views, errors, forms
