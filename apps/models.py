from datetime import datetime
from time import mktime

from sqlalchemy.orm import backref

from apps import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# current_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 基类：添加时间
class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间(登录时间)


# 用户类
class User(UserMixin, BaseModel, db.Model):
    """用户"""

    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户暱称
    authority = db.Column(db.String(2), unique=False, default=0)  # 用户权限0<1<2
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码

    # create_time
    # update_time

    # server_threshold = db.relationship('ServerThreshold', backref='user_3', lazy='dynamic')  # 对应用户管理的服务器

    # 希望再提供一个password属性, 能够直接进行密码的设置
    # @property: 将下面的函数提升为属性(getter)
    @property
    def password(self):
        raise AttributeError('不允许访问密码')

    @password.setter
    def password(self, value):
        # 在属性的setter方法中进行密码加密处理
        self.password_hash = generate_password_hash(value)

    # 检查密码是否一致
    def check_password(self, value):
        """检查用户密码，value是用户填写密码"""
        return check_password_hash(self.password_hash, value)

    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "authority": self.authority,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

    def auth_to_dict(self):
        """将实名信息转换为字典数据"""
        auth_dict = {
            "user_id": self.id,
            "user_name": self.name
        }
        return auth_dict

    def __repr__(self):
        str_ = '用户名 name:{name}'.format(name=self.name)
        return str_


# 操作日志类
class OperationLog(BaseModel, db.Model):
    """操作日志"""

    __tablename__ = "operation_log"

    id = db.Column(db.Integer, primary_key=True)  # 操作编号
    module = db.Column(db.String(8))  # 操作模块
    operation = db.Column(db.String(128))  # 执行的操作
    operation_res = db.Column(db.String(32))  # 操作结果
    # create_time 已继承
    update_time = None  # 取消update字段

    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))  # 外键关联user
    users = db.relationship('User', backref=backref('operation'), foreign_keys=[user_id])  # 对应用户的操作日志

    def to_dict(self):
        """将对象转换为字典数据"""
        # 根据前端的需求, 返回对应字段的信息
        operation_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "module": self.module,
            "operation": self.operation,
            "res": self.operation_res,
            "time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return operation_dict

    def __repr__(self):
        str_ = "OperationLog(id={id},user_id={user_id})".format(id=self.id, user_id=self.user_id)
        return str_


# 告警日志类
class AlertLog(BaseModel, db.Model):
    """告警日志"""

    __tablename__ = "alert_log"

    id = db.Column(db.Integer, primary_key=True)  # 操作编号
    threshold = db.Column(db.String(8))  # 设定阈值
    recording = db.Column(db.String(8))  # 记录值
    type = db.Column(db.String(16))  # 告警类型
    desc = db.Column(db.String(32))  # 描述(执行操作)
    # create_time 已继承
    update_time = None  # 取消update字段

    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))
    servers = db.relationship('ServerInfo', backref=backref('alert_log'), foreign_keys=[server_id])

    def to_dict(self):
        """将对象转换为字典数据"""
        alert_dict = {
            "id": self.id,
            "s_id": self.server_id,
            "th": self.threshold,
            "record": self.recording,
            "type": self.type,
            "desc": self.desc,
            "time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return alert_dict

    def __repr__(self):
        str_ = """
        AlertLog类
        alert_log
        包含字段：
        id
        server_id
        threshold
        recording 
        server_ip 
        type
        desc
        create_time
        """
        return str_


# 服务器配置类
class ServerInfo(BaseModel, db.Model):
    """服务器信息
    # - 服务器名称
    # - ip
    # - 端口
    # - 操作系统
    # - 描述
    # - ssh用户名【界面上不显示】
    # - ssh密码（明文）【界面上显示】"""

    __tablename__ = "server_info"

    id = db.Column(db.Integer, primary_key=True)  # 服务器编号
    name = db.Column(db.String(32), nullable=False)  # 服务器名称
    server_ip = db.Column(db.String(32))  # 服务器ip
    server_port = db.Column(db.String(6))  # 服务器端口
    server_os = db.Column(db.String(32))  # 操作系统
    server_desc = db.Column(db.String(128))  # 描述
    ssh_name = db.Column(db.String(128))  # ssh用户名
    ssh_password = db.Column(db.String(128))  # ssh密码，明文
    state = db.Column(db.Boolean, default=False)  # 监听状态
    # create_time
    # update_time

    # 外键user_id
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    users = db.relationship('User', backref=backref('server'), foreign_keys=[user_id])

    def to_dict(self):
        """将对象转换为字典数据"""
        # 根据前端的需求, 返回对应字段的信息
        server_dict = {
            'id': self.id,
            "name": self.name,
            "server_ip": self.server_ip,
            "server_port": self.server_port,
            "server_os": self.server_os,
            "server_desc": self.server_desc,
            "ssh_name": self.ssh_name,
            "ssh_password": self.ssh_password,
            "state": self.state,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time
        }
        return server_dict

    def __repr__(self):
        str = """
        ServerInfo类
        id:{id}
        """.format(id=self.id)
        return str


# 告警阈值设置表
class ServerThreshold(BaseModel, db.Model):
    """告警阈值设置"""

    __tablename__ = "server_threshold"

    id = db.Column(db.Integer, primary_key=True)  # 服务器编号
    server_mem_th = db.Column(db.String(3), default='0')  # 内存阈值
    server_cpu_th = db.Column(db.String(3), default='0')  # cpu阈值
    server_disk_th = db.Column(db.String(3), default='0')  # 磁盘阈值

    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))
    servers = db.relationship('ServerInfo', backref=backref('threshold', uselist=False, cascade='all,delete'),
                              foreign_keys=[server_id])

    # create_time
    # update_time

    def to_dict(self):
        threshold_dict = {
            "id": self.id,
            "s_id": self.server_id,
            "s_mem_th": self.server_mem_th,
            "s_cpu_th": self.server_cpu_th,
            "s_disk_th": self.server_disk_th
        }
        return threshold_dict

    def __repr__(self):
        str_ = """
        ServerThreshold表
        id:{id}
        """.format(id=self.id)
        return str_


class LatestServerInfo(BaseModel, db.Model):
    """服务器近况"""

    __tablename__ = "latest_info"

    id = db.Column(db.Integer, primary_key=True)  # 服务器编号

    cpu_rate = db.Column(db.String(5), default='0')  # cpu

    mem_total = db.Column(db.String(16), default='0')  # 内存
    mem_free = db.Column(db.String(16), default='0')  # 内存
    mem_used_rate = db.Column(db.String(5), default='0')  # 内存

    disk_total = db.Column(db.String(16), default='0')  # 磁盘
    disk_size = db.Column(db.String(16), default='0')  # 磁盘
    disk_used_rate = db.Column(db.String(5), default='0')  # 磁盘

    loadIn1Min = db.Column(db.String(5), default='0')  # 1分钟负载
    loadIn5Min = db.Column(db.String(5), default='0')  # 5分钟负载
    loadIn10Min = db.Column(db.String(5), default='0')  # 10分钟负载

    server_id = db.Column(db.Integer, db.ForeignKey('server_info.id'))
    servers = db.relationship('ServerInfo', backref=backref('latest', uselist=False, cascade='all,delete'),
                              foreign_keys=[server_id])

    # create_time
    # update_time

    def to_dict(self):
        return {
            'id': self.id,
            'cpu_rate': self.cpu_rate,
            'mem_used_rate': self.mem_used_rate,
            'disk_used_rate': self.disk_used_rate,
            # 'loadIn1Min': self.loadIn1Min
        }

    def __repr__(self):
        str_ = """
            LatestServerInfo表
            id:{id}
            """.format(id=self.id)
        return str_
