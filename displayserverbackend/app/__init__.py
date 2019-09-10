#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import logging

from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()


def create_app(config_name=None):
    if config_name is None:
        config_name = 'development'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, async_mode="threading")

    app.logger.setLevel(logging.INFO)

    return app


from app import routes
