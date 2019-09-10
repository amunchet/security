#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import os

from flask import current_app

from app.emulator import CameraEmulator
from app.models import ImageGenerator, FtpClient


def create_image_generator():
    images_repo_path = os.path.join(current_app.root_path, 'images-repo')
    frequency = current_app.config['IMG_GEN_FREQUENCY']
    return ImageGenerator(frequency, images_repo_path)


def create_camera_emulator():
    camera_name = current_app.config['CAM_NAME']
    generated_image_path = os.path.join(current_app.root_path, 'generated-image')

    ce = CameraEmulator(camera_name, create_image_generator(), generated_image_path)
    if current_app.config['FTP_SUPPORTED'] == 'true':
        host = current_app.config['FTP_HOST']
        user = current_app.config['FTP_USER']
        password = current_app.config['FTP_PASSWORD']
        ftp_client = FtpClient(host, user, password)
        ce.set_ftp_client(ftp_client)
    return ce
