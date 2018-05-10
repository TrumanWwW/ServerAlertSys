# -*- coding:utf-8 -*-
# 配置参数

class Config(object):
    # 调试模式 SECRET_KEY MYSQL Redis Session
    # MYSQL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/server_alarm_sys_lite_db'
    # 跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 查询时显示sql语句
    SQLALCHEMY_ECHO = True
    # 自动commit
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 使用本地bootstrap
    BOOTSTRAP_SERVE_LOCAL = True

    # 配置SECREK_KEY
    '''
    import os
    import base64
    base64.b64encode(os.urandom(32))
    '''
    SECRET_KEY = 'kirZAfCoxKJWk7w+7dBRbZJIItZ97YXynGqbrqsXQMI='


class DevelopmentConfig(Config):
    """开发环境配置"""
    # 调试模式
    DEBUG = True
    # 查询时显示sql语句
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """生产环境配置"""
    # 暂时用不上, 如果需要, 填入对应配置信息
    pass


# 提供一个字典, 绑定关系
config_dict = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}