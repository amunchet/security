#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import logging

from flask import Flask

from config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = 'development'
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    app.logger.setLevel(logging.INFO)

    return app

