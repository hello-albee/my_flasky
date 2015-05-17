#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python D:\GitHub\my_flasky\hello.py runserver --host 0.0.0.0
# test.flasky@gmail.com

import os
from threading import Thread
from datetime import datetime
from flask import Flask,render_template, session, redirect, url_for, flash
from flask.ext.script import Manager,Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)


manager = Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
r'''
(venv) PS C:\Users\bobo> python D:\GitHub\my_flasky\hello.py shell
>>> from flask.ext.mail import Message
>>> from hello import mail
>>> msg=Message('test subject',sender='sender@example.com',recipients=['cnnic17173@163.com'])
>>> msg.body='text body' # 似乎没有用
>>> msg.html='<b>HTML</b> body'
>>> with app.app_context():
...     mail.send(msg)
...
>>>
'''

if __name__ == '__main__':
    manager.run()
