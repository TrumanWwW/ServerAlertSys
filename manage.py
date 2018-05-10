# 只负责程序的启动

from apps import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 实际上, 程序的运行时需要区分开发模式和发布模式的. 这个模式的控制, 也应该交由manage来管理

# product/develop
app, db = create_app('develop')

# 创建manager
manager = Manager(app)
# 创建迁移对象
migrate = Migrate(app, db)
# 给manager添加db命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
    # from waitress import serve
    # serve(app, listen='127.0.0.1:5000')
    # serve(app, listen='127.0.0.1:5000', host='0.0.0.0')
