# -*- coding: utf-8 -*-
# 服务器信息的获取，信息概览接口实现
import logging

import paramiko
import re

# from . import api
from apps.models import ServerInfo

# from apps.utils.commons import login_required

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

'''
    结果 可以直接显示在界面上，客户端 5秒刷新一下
'''


# 操作服务器，获取各种参数
class Tool(object):
    def __init__(self):

        self.host_list = []

        # self.host_list = [
        #     {
        #         'ip': '192.168.120.2',
        #         'port': 22,
        #         'username': 'root',
        #         'password': '123456'
        #     }, {
        #         'ip': '192.168.110.80',
        #         'port': 22,
        #         'username': 'root',
        #         'password': '123456'
        #     }, {
        #         'ip': '192.168.110.88',
        #         'port': 22,
        #         'username': 'root',
        #         'password': '123456'
        #     }
        # ]

    @staticmethod
    def con_ssh(ip, port, username, password):
        ssh.connect(hostname=ip, port=port, username=username, password=password, timeout=1)

    @staticmethod
    def close_ssh():
        ssh.close()

    def get_menu(self):

        # 查询数据库表server_info
        server_info_list = ServerInfo.query.all()  # 查询到一个包含所有服务器信息的list
        for i in server_info_list:
            info = {
                'id': i.id,
                'ip': i.server_ip,
                'port': i.server_port,
                'username': i.ssh_name,
                'password': i.ssh_password
            }
            self.host_list.append(info)

        server_info = list()
        for host in self.host_list:
            # 尝试访问服务器
            try:
                self.con_ssh(host['ip'], host['port'], host['username'], host['password'])

            # 服务器访问超时或者异常
            except Exception as e:
                logging.info('服务器:' + str(host['ip']) + "访问失败")
                info = {
                    'id': host['id'],
                    'ip': host['ip'],
                    'port': host['port'],
                    'username': host['username'],
                    'password': host['password'],
                    'status': '连接失败'
                }
                server_info.append({
                    'info': info
                })
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
                # 服务器负载监控load average分别对应于过去1分钟，5分钟，15分钟的负载平均值
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
                    logging.info(mem_menu_err)
                    return mem_menu_err
                if cpu_menu_err:
                    logging.info(cpu_menu_err)
                    return cpu_menu_err
                if cpu_menu_err2:
                    logging.info(cpu_menu_err2)
                    return cpu_menu_err2
                if disk_menu_err:
                    logging.info(disk_menu_err)
                    return disk_menu_err
                if load_menu_err:
                    logging.info(load_menu_err)
                    return load_menu_err

                # self.close_ssh()

                # 内存
                # print(mem_menu_out)
                # 物理内存
                total_mem = re.search('MemTotal:\s*(\d*).*?\n', mem_menu_out).group(1)
                free_mem = re.search('MemFree:\s*(\d*).*?\n', mem_menu_out).group(1)
                mem_used_rate = round((int(total_mem) - int(free_mem)) / int(total_mem) * 100, 1)
                # 虚拟内存
                v_total_mem = re.search('VmallocTotal:\s*(\d*).*?\n', mem_menu_out).group(1)
                v_used_mem = re.search('VmallocUsed:\s*(\d*).*?\n', mem_menu_out).group(1)
                v_mem_used_rate = round(int(v_used_mem) / int(v_total_mem) * 100, 1)
                mem = {
                    'mem_total': round(int(total_mem) / 1024 / 1024, 2),
                    'mem_used': round((int(total_mem) - int(free_mem)) / 1024 / 1024, 2),
                    'mem_rate': mem_used_rate
                }
                vmem = {
                    'vmem_total': round(int(v_total_mem) / 1024 / 1024, 2),
                    'vmem_used': round(int(v_used_mem) / 1024 / 1024, 2),
                    'vmem_rate': v_mem_used_rate
                }
                # print(mem)
                # print(vmem)

                # CPU
                # print(cpu_menu_out2)
                cpu_model = re.search(r'Model name:\s*(.*?)\n', cpu_menu_out).group(1)
                cpu_free = re.search(r'Average:\s*(.*?)\n', cpu_menu_out2).group(1)
                cpu_free = re.split('\s+', cpu_free)[-1]
                cpu = {
                    'cpu_model': cpu_model,
                    'cpu_free': cpu_free
                }
                # print(cpu)

                # 磁盘
                # print(disk_menu_out)
                disk_line = re.split(r'\n', disk_menu_out)[-2]
                disk_line_list = re.split('\s+', disk_line)
                disk_used = disk_line_list[2]
                disk_size = disk_line_list[1]
                disk_use_rate = disk_line_list[-2]
                disk = {
                    'disk_used': disk_used,
                    'disk_size': disk_size,
                    'disk_use': disk_use_rate,
                }
                # print(disk)

                # 服务器负载
                # print(load_menu_out)
                load = re.search(r'load average:\s*(.*)\s*\n', load_menu_out).group(1)
                load = re.split(r'\s*,\s*', load)
                loadIn1Min = load[0]
                loadIn10Min = load[1]
                loadIn15Min = load[2]
                load = {
                    'loadIn1Min': loadIn1Min,
                    'loadIn10Min': loadIn10Min,
                    'loadIn15Min': loadIn15Min
                }
                # print(load)
                # 服务器信息
                info = {
                    'id': host['id'],
                    'ip': host['ip'],
                    'port': host['port'],
                    'username': host['username'],
                    'password': host['password'],
                    'status': '在线'
                }
                server_info.append({
                    'mem': mem,
                    'cpu': cpu,
                    'disk': disk,
                    'load': load,
                    'vmem': vmem,
                    'info': info
                })
                # print('-----------------------------')

        # print(server_info)
        return server_info

if __name__ == '__main__':
    tool = Tool()
    tool.get_menu()
