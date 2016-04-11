# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from sqlalchemy import or_

from . import db
from .models import User
from .tasks import send_async_mail

main_bp = Blueprint('main', __name__)


@main_bp.route('/', endpoint='index', methods=['GET', 'POST'])
def index_view():
    if request.method.lower() == 'post':
        # 获取表单
        username = request.form['username']
        email = request.form['email']
        u = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not u:
            # 创建用户
            u = User(username=username, email=email)
            db.session.add(u)
            db.session.commit()
        return redirect(url_for('.index'))

    users = User.query.all()
    return render_template('index.html', users=users)


@main_bp.route('/send-mail/<username>', endpoint='send_mail')
def send_mail_view(username):
    u = User.query.filter_by(username=username).first_or_404()
    send_async_mail.delay(u.email, 'Test Mail', 'mail.html',
                          username=u.username, now=datetime.now())
    return redirect(url_for('.index'))
