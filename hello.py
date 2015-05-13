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
app.config['SECRET_KEY'] = 'let me guess'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://scott:tiger@127.0.0.1:3306/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465 # 使用SSL加密的时候采用此端口
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[From_my_Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Admin<test.flasky@gmail.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN') # test_flask@sina.com




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

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

def send_async_email(app, msg): # 异步发送电子邮件
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

class NameForm(Form):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context)) # 注册一个make_context回调函数
manager.add_command('db', MigrateCommand)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                # pass
                send_email(app.config['FLASKY_ADMIN'], 'New User Add','mail/add_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',current_time=datetime.utcnow(),form=form,name=session.get('name'),known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__ == '__main__':
    manager.run()
