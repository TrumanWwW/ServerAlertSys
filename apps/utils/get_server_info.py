# -*- coding: utf-8 -*-
# 循环依次查询服务器列表中服务器，保存实时信息，并做阈值判断，输出告警
# import logging
from datetime import datetime
from threading import Timer

import paramiko
import re

from apps import db, create_app
from apps.models import ServerInfo, LatestServerInfo, ServerThreshold, AlertLog
from apps.utils.record_log import record_alert_log

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


# 操作服务器，获取各种参数
class Tool(object):
    def __init__(self):

        self.host_list = []

    @staticmethod
    def con_ssh(ip, port, username, password):
        ssh.connect(hostname=ip, port=port, username=username, password=password, timeout=1)

    @staticmethod
    def close_ssh():
        ssh.close()

    def get_data(self):
        """脚本检测所有服务器信息并存入数据库"""
        # 查询数据库表server_info
        servers = ServerInfo.query.all()  # 查询到一个包含所有服务器信息的list

        for i in servers:
            info = {
                'id': i.id,
                'ip': i.server_ip,
                'port': i.server_port,
                'username': i.ssh_name,
                'password': i.ssh_password
            }
            self.host_list.append(info)
        for host in self.host_list:
            # 尝试访问服务器
            try:
                self.con_ssh(host['ip'], host['port'], host['username'], host['password'])

            # 服务器访问超时或者异常
            except Exception as e:
                # self.close_ssh()
                default_set = {
                    'cpu_rate': '--',
                    'mem_total': '--',
                    'mem_free': '--',
                    'mem_used_rate': '--',
                    'disk_total': '--',
                    'disk_size': '--',
                    'disk_used_rate': '--',
                    'loadIn1Min': '--',
                    'loadIn5Min': '--',
                    'loadIn10Min': '--',
                    'server_id': host['id']
                }
                latest = LatestServerInfo.query.filter_by(server_id=host['id']).first()
                if latest:
                    for k, v in default_set.items():
                        setattr(latest, k, v)
                else:
                    db.session.add(LatestServerInfo(**default_set))
                db.session.commit()
            # 服务器访问正常
            else:
                # 执行内存查看指令
                mem_menu_in, mem_menu_out, mem_menu_err = ssh.exec_command('cat /proc/meminfo')
                # 执行cpu查看指令'cat /proc/cpuinfo'
                cpu_menu_in, cpu_menu_out, cpu_menu_err = ssh.exec_command('lscpu')
                # 读取cpu使用率[sar -u 每一秒统计一次 总计2次]
                cpu_menu_in2, cpu_menu_out2, cpu_menu_err2 = ssh.exec_command('sar -u 1 2')
                # 查看磁盘根目录使用情况
                disk_menu_in, disk_menu_out, disk_menu_err = ssh.exec_command('df -h /')
                # 服务器负载监控load average分别对应于过去1分钟，5分钟，15分钟的负载值
                load_menu_in, load_menu_out, load_menu_err = ssh.exec_command('w')

                # 读取内存信息
                mem_menu_out = mem_menu_out.read().decode()
                mem_menu_err = mem_menu_err.read().decode()
                # 读取cpu信息
                cpu_menu_out = cpu_menu_out.read().decode()
                cpu_menu_err = cpu_menu_err.read().decode()
                # 读取cpu信息
                cpu_menu_out2 = cpu_menu_out2.read().decode()
                cpu_menu_err2 = cpu_menu_err2.read().decode()
                # 读取磁盘信息
                disk_menu_out = disk_menu_out.read().decode()
                disk_menu_err = disk_menu_err.read().decode()
                # 读取负载信息
                load_menu_out = load_menu_out.read().decode()
                load_menu_err = load_menu_err.read().decode()

                if mem_menu_err:
                    # logging.info(mem_menu_err)
                    return mem_menu_err
                if cpu_menu_err:
                    # logging.info(cpu_menu_err)
                    return cpu_menu_err
                if cpu_menu_err2:
                    # logging.info(cpu_menu_err2)
                    return cpu_menu_err2
                if disk_menu_err:
                    # logging.info(disk_menu_err)
                    return disk_menu_err
                if load_menu_err:
                    # logging.info(load_menu_err)
                    return load_menu_err

                # 内存
                total_mem = re.search('MemTotal:\s*(\d*).*?\n', mem_menu_out).group(1)
                free_mem = re.search('MemFree:\s*(\d*).*?\n', mem_menu_out).group(1)
                mem_used_rate = round((int(total_mem) - int(free_mem)) / int(total_mem) * 100, 1)

                # 'cpu_rate': '68.84'
                cpu_free = re.search(r'[(\u5e73\u5747\u65f6\u95f4)|(Average)]:\s*(.*?)\n', cpu_menu_out2).group(1)
                cpu_free = re.split('\s+', cpu_free)[-1]
                cpu_free = round(100.00 - float(cpu_free), 2)
                # 磁盘
                # 'disk_used': '6.3G', 'disk_size': '76G', 'disk_use': '9%'
                disk_line = re.split(r'\n', disk_menu_out)[-2]
                disk_line_list = re.split('\s+', disk_line)

                # 服务器负载
                load = re.search(r'load average:\s*(.*)\s*\n', load_menu_out).group(1)
                load = re.split(r'\s*,\s*', load)

                default_set = {
                    'cpu_rate': cpu_free,
                    'mem_total': round(int(total_mem) / 1024 / 1024, 2),
                    'mem_free': round(int(free_mem) / 1024 / 1024, 2),
                    'mem_used_rate': mem_used_rate,
                    'disk_total': disk_line_list[1],
                    'disk_size': disk_line_list[2],
                    'disk_used_rate': round(float(disk_line_list[2][:-1]) / float(disk_line_list[1][:-1]) * 100, 2),
                    'loadIn1Min': load[0],
                    'loadIn5Min': load[1],
                    'loadIn10Min': load[2],
                    'server_id': host['id']
                }
                latest = LatestServerInfo.query.filter_by(server_id=host['id']).first()

                # 保存状态到数据库
                if latest:
                    for k, v in default_set.items():
                        setattr(latest, k, v)
                else:
                    db.session.add(LatestServerInfo(**default_set))
                db.session.commit()

                # 产生告警
                server_t = ServerThreshold.query.filter_by(server_id=host['id']).first()
                # 未开启监听
                if not server_t.servers.state:
                    return False

                if float(default_set['mem_used_rate']) > float(server_t.server_mem_th):
                    a_log = AlertLog.query \
                        .filter_by(server_id=host['id'], type='mem') \
                        .order_by('alert_log.id desc').first()
                    if not a_log or (datetime.now() - a_log.create_time).seconds > (3 * 60):
                        record_alert_log(server_t.server_mem_th,
                                         default_set['mem_used_rate'],
                                         'mem',
                                         u'内存占用超出设定阈值',
                                         host['id'])
                if float(default_set['cpu_rate']) > float(server_t.server_cpu_th):
                    a_log = AlertLog.query \
                        .filter_by(server_id=host['id'], type='cpu') \
                        .order_by('alert_log.id desc').first()
                    if not a_log or (datetime.now() - a_log.create_time).seconds > (3 * 60):
                        record_alert_log(server_t.server_cpu_th,
                                         default_set['cpu_rate'],
                                         'cpu',
                                         u'CPU使用超出设定阈值',
                                         host['id'])
                if float(default_set['disk_used_rate']) > float(server_t.server_disk_th):
                    a_log = AlertLog.query \
                        .filter_by(server_id=host['id'], type='disk') \
                        .order_by('alert_log.id desc').first()
                    if not a_log or (datetime.now() - a_log.create_time).seconds > (3 * 60):
                        record_alert_log(server_t.server_disk_th,
                                         default_set['disk_used_rate'],
                                         'disk',
                                         u'磁盘占用超出设定阈值',
                                         host['id'])


def fn():
    app = create_app('develop')  # 创建一个app用于检测
    tool = Tool()
    tool.get_data()


def run():
    Timer(5, fn).start()


if __name__ == '__main__':
    tool = Tool()
    tool.get_data()
