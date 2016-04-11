# -*- coding: utf-8 -*-

import os

from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_script import Shell

from app import create_app
from app import db

app = create_app(os.getenv('APP_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    from app.models import User
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def develop(host='0.0.0.0', port=5000):
    """Run the develop server"""
    app.run(host=host, port=port, debug=True, threaded=True)


if __name__ == '__main__':
    manager.run()
