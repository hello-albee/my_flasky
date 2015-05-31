#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'let me guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465 # 使用SSL加密的时候采用此端口
    MAIL_PORT = 587
    # app.config['MAIL_USE_SSL'] = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[牛斯狗评论]'
    FLASKY_MAIL_SENDER = '牛斯狗评论管理员<test.flasky@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') # test_flask@sina.com
    Moderator = os.environ.get('Moderator') #
    FLASKY_POSTS_PER_PAGE=25 # 每页显示的记录数
    FLASKY_FOLLOWERS_PER_PAGE=20
    


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI ='mysql://scott:tiger@127.0.0.1:3306/Development'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI ='mysql://scott:tiger@127.0.0.1:3306/test'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI ='mysql://scott:tiger@127.0.0.1:3306/Production'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
