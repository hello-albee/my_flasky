#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from app import create_app, db
from app.models import User, Role
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('default') # 默认为开发
# app = create_app('testing')
# app = create_app('production')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context)) # 注册一个make_context回调函数
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """单元测试."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
