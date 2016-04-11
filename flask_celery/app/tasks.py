# -*- coding: utf-8 -*-

from datetime import datetime

from flask import render_template
from flask_mail import Message

from . import mail
from . import make_celery

celery = make_celery()


@celery.task(name='send_mail', base=celery.Task, bind=True)
def send_async_mail(self, to, subject, template, **kwargs):
    """发送邮件

    :param to: 收件人
    :type to: str | tuple

    :param subject: 邮件主旨
    :type subject: str

    :param template: 邮件模板
    :type template: str
    """
    recipients = to if isinstance(to, (list, tuple)) else [to]
    msg = Message(subject=subject, recipients=recipients)
    msg.html = render_template(template, **kwargs)
    mail.send(msg)


@celery.task(name='print_time', base=celery.Task, bind=True)
def print_time(self, utc_time=True):
    """打印当前时间

    :param utc_time: 打印utc时间
    :type utc_time: bool
    """
    print(datetime.utcnow() if utc_time else datetime.now())
