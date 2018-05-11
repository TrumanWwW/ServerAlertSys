# -*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from .utils.commons import RegexConverter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_dict

# 惰性加载
db = SQLAlchemy()
bootstrap = Bootstrap()
# LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message = {'errors': {'e': [u"您还未登录!"]}}
login_manager.login_view = 'auth.login'
# 定义redis_store对象, 先设置为None
# redis_store = None

'''
日志的级别
ERROR: 错误级别
WARN: 警告级别
INFO: 信息界别
DEBUG: 调试级别
平时开发, 可以使用debug和info替代print, 来查看对象的值
上线时, 不需要删除这个日志, 只需要更改日志的级别为error/warn
'''
# 设置日志的记录等级
logging.basicConfig(level=logging.WARN)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 5, backupCount=10)
# 创建日志记录的格式(时间 - 日志等级 - 输入日志信息的文件名 - 行数 - 日志信息)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """用于创建app及其配置"""

    # 创建app
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    app.app_context().push()

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # 初始化db对象
    # 作用域问题处理，在函数外创建db对象，提升作用域
    # 某些对象需要外界调用. 可以延迟传参

    # app.app_context().push()

    # 向app中添加自定义的路由转换器
    app.url_map.converters['re'] = RegexConverter

    # 注册蓝图
    # 为了解决蓝图循环导入的问题, 也可以延迟导入
    from apps.main import main
    app.register_blueprint(main)
    from apps.auth import auth
    app.register_blueprint(auth)
    from apps.api_v1 import api
    app.register_blueprint(api, url_prefix='/api_v1')

    # 监听服务器

    from apps.utils import get_server_info
    get_server_info.run()
    # 创建Session, 将session数据从以前默认的cookie, 存放到redis中
    # http://pythonhosted.org/Flask-Session/ 教程
    # 这里需要返回APP对象，和db
    return app, db

