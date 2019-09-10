#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    PORT = os.environ.get('PORT') or 5000
    # FTP configuration
    FTP_SUPPORTED = os.environ.get('FTP_SUPPORTED') or False
    FTP_HOST = os.environ.get('FTP_HOST') or 'localhost'
    FTP_USER = os.environ.get('FTP_USER')
    FTP_PASSWORD = os.environ.get('FTP_PASSWORD')

    # Frequency of image generation in seconds
    IMG_GEN_FREQUENCY = os.environ.get('IMG_GEN_FREQUENCY') or 1

    # Unique name of the camera
    CAM_NAME = os.environ.get('CAM_NAME')


class DevelopmentConfig(Config):
    # DEBUG = True
    pass


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    FTP_SUPPORTED = "true"
    FTP_HOST = "localhost"
    FTP_USER = 'admin'
    FTP_PASSWORD = 'pass'
    CAM_NAME = "camera_1"


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
