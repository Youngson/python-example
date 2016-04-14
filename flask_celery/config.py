# -*- coding: utf-8 -*-

import os

from celery.schedules import crontab

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret.key')

    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND',
                                      'db+sqlite:///{0}'.format(
                                          os.path.join(base_dir, 'celery.db')))
    CELERYBEAT_SCHEDULE = {
        'every_one_minutes_print_utc_time': {
            'task': 'print_time',
            'schedule': crontab(),
            'args': (True,)
        },
        'every_two_minutes_print_time': {
            'task': 'print_time',
            'schedule': crontab(minute='*/2'),
            'args': (False,)
        }
    }

    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URI',
        'sqlite:///{0}'.format(os.path.join(base_dir, 'dev_db.db'))
    )
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URI',
        'sqlite:///:memory:'
    )
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URI',
        'sqlite:///{0}'.format(os.path.join(base_dir, 'db.db'))
    )
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
