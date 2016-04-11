# -*- coding: utf-8 -*-

from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return self.username
