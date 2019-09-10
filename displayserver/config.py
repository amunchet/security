#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FTP configuration
    FTP_HOST = os.environ.get('FTP_HOST') or 'localhost'
    FTP_USER = os.environ.get('FTP_USER')
    FTP_PASSWORD = os.environ.get('FTP_PASSWORD')


class DevelopmentConfig(Config):
    #DEBUG = True
    pass

class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    FTP_USER = 'admin'
    FTP_PASSWORD = 'pass'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
