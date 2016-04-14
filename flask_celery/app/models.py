# -*- coding: utf-8 -*-

from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return self.username


class CeleryTask(db.Model):
    __tablename__ = 'celery_task'

    id = db.Column(db.String(64), primary_key=True)
    func = db.Column(db.String(64))
    send_time = db.Column(db.DateTime, default=datetime.utcnow)
    params = db.Column(db.Text)
