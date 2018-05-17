# 服务器监测软件

[TOC]

## 1.目标

​	对服务器的处理器、内存、磁盘进行监控

## 2.功能

 - 可视化仪表
 - 用户配置
 - 服务器配置
 - 服务器阈值
 - 日志（操作、告警）

## 3.环境

### 硬件环境

略

### 软件环境

- 系统环境:windows10


- ide:pycharm

- 编译器:python 3.6

- 依赖:见requirements.txt

- 数据库:mysql5.7.21(mysql://root:mysql@127.0.0.1/server_alarm_system_db)

## 4.文档结构
```
ServerAlarmSysLite
	│
	│  config.py ---- 配置文件
	│  manage.py ---- 启动文件
	│  README.md ---- 说明
	│  requirements.txt ---- 依赖包
	│  
	├─apps
	│  │  models.py ---- SQLAchemey模型
	│  │  __init__.py
	│  │  
	│  ├─api_v1 ---- 接口文件夹
	│  │  │  conf.py ---- 配置接口
	│  │  │  dashboard.py ---- 首页接口
	│  │  │  log.py ---- 首页接口
	│  │  │  users.py ---- 用户管理接口
	│  │  └─ __init__.py
	│  │          
	│  ├─auth ---- 登录模块
	│  │  │  forms.py ---- 表单类
	│  │  │  views.py ---- 视图
	│  │  └─ __init__.py
	│  │          
	│  ├─main ---- 主视图文件夹
	│  │  │  errors.py
	│  │  │  forms.py ---- 表单类
	│  │  │  views.py ---- 主视图
	│  │  └─ __init__.py
	│  │          
	│  ├─static
	│  │  │  favicon.ico
	│  │  │  
	│  │  ├─css ---- 样式
	│  │  │  │  public.css
	│  │  │  │  
	│  │  │  ├─auth
	│  │  │  └─dashboard
	│  │  │          dashboard.css
	│  │  │          
	│  │  ├─img
	│  │  │      server_monitor.svg
	│  │  │      
	│  │  ├─js ---- JS
	│  │  │  │  public.js
	│  │  │  │  
	│  │  │  ├─config
	│  │  │  │      config_alert.js
	│  │  │  │      config_server.js
	│  │  │  │      
	│  │  │  ├─dashboard
	│  │  │  │      dashboard.js
	│  │  │  │      
	│  │  │  ├─log
	│  │  │  │      alert.js
	│  │  │  │      operation.js
	│  │  │  │      
	│  │  │  └─users
	│  │  │          users.js
	│  │  │          
	│  │  ├─lib
	│  │  │      MouseWheel.js
	│  │  │      
	│  │  └─third_party ---- 第三方插件
	│  │ 
	│  ├─templates ---- 模板文件夹
	│  │  │  403.html
	│  │  │  404.html
	│  │  │  500.html
	│  │  │  base.html
	│  │  │  macro_alert.html
	│  │  │  macro_form_toolbar.html
	│  │  │  
	│  │  ├─auth
	│  │  │      login.html
	│  │  │      
	│  │  ├─config
	│  │  │      alert.html
	│  │  │      server.html
	│  │  │      
	│  │  ├─dashboard
	│  │  │      dashboard.html
	│  │  │      
	│  │  ├─log
	│  │  │      alert.html
	│  │  │      operation.html
	│  │  │      
	│  │  └─users
	│  │          users.html
	│  │          
	│  └─utils ---- 自定义工具包
	│     │  commons.py
	│     │  get_server_info.py
	│     │  record_log.py
	│     └─ __init__.py 
	│          
	├─logs ---- 应用日志
	│      
	├─migrations ---- 迁移目录
	│          
	└─venv ---- 虚拟环境
```



## 5.安装

> 以Debian系为例

- 安装python3.6

  - `$sudo apt install python3.6`

  - 安装pip3`$ sudo apt-get install python3-pip`

  - 安装virtualenv

    - `$ pip3 install virtualenv`

    - `$ pip3 install virtualenvwrapper`

    - ~/.bashrc文件末尾添加

      ```
      export WORKON_HOME=$HOME/.virtualenvs 
      # 存在python3和python2时
      export VERTUALENVWRAPPER_PYTHON = /usr/bin/python3
      source /usr/local/bin/virtualenvwrapper.sh
      ```
    - 执行`source ~/.bashrc`

  - 进入虚拟环境

    - `$ mkvirtualenv ServerAlertSysLite`
    - 安装依赖包`$ pip install -r requirements.txt`

- mysql

  - 安装`$ sudo apt install mysql-server`
  - 进入`$ mysql`
  - 执行`CREATE DATABASE server_alarm_system_db CHARSET=UTF8;`

- 控制台输入

  - `python manage.py` 启动服务器

## 6.数据库E-R

![E-R图](https://note.youdao.com/yws/public/resource/49419d5db1b287ed357e5391ac3f68de/xmlnote/1FE1551C30AF495CAE8D1A1798DB56F0/10625)

## 7.使用

- 启动
  - 控制台输入`python manage.py` ，默认127.0.0.1:5000，可在`manage.py`中更改


- 登录、注册

  - `/login`
- 配置
  - 服务器配置`/config/server`：配置对应服务器
  - 告警配置`/config/alert`：对当前用户分配到的服务器，做告警配置
- 用户管理`/users`
- 操作日志`/log/operation`：显示用户操作
- 报警日志`/log/alert`：显示服务器超过阈值信息

## 8.已知问题

1. 用户权限更改限制