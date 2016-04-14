# -*- coding: utf-8 -*-

from datetime import datetime
import json

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from sqlalchemy import or_

from . import db
from .models import CeleryTask
from .models import User
from .tasks import celery
from .tasks import send_async_mail

main_bp = Blueprint('main', __name__)


def get_task_state(task_id):
    """获取任务状态"""
    return celery.AsyncResult(task_id).state


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


@main_bp.app_context_processor
def inject_object():
    return {
        'get_task_state': get_task_state,
        'json': json
    }


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
    tasks = CeleryTask.query.order_by(CeleryTask.send_time.desc()).all()
    return render_template('index.html', users=users, tasks=tasks)


@main_bp.route('/send-mail/<username>', endpoint='send_mail')
def send_mail_view(username):
    u = User.query.filter_by(username=username).first_or_404()
    params = dict(to=u.email, subject='Test Mail', template='mail.html',
                  username=u.username, now=datetime.now())

    rv = send_async_mail.delay(**params)

    t = CeleryTask(id=rv.task_id, func='send_async_mail',
                   params=json.dumps(params, default=date_handler))
    db.session.add(t)
    db.session.commit()
    return redirect(url_for('.index'))
