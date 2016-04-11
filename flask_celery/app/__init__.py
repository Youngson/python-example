# -*- coding: utf-8 -*-

import os

from celery import Celery
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
mail = Mail()


def create_app(config_name, register_blueprint=True):
    """创建flask应用

    :param config_name: 配置键
    :type config_name: str

    :param register_blueprint: 是否注册蓝图
    :type register_blueprint: bool

    :return: flask.Flask
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    mail.init_app(app)

    if register_blueprint:
        from .views import main_bp
        app.register_blueprint(main_bp)

    from . import models

    return app


def make_celery(app=None):
    """创建celery

    :param app: flask应用
    :type app: flask.Flask

    :return: celery.Celery
    """
    app = app or create_app(os.getenv('APP_CONFIG', 'default'), False)
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super(ContextTask, self).__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery
