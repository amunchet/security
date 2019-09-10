#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import base64
import os
import time

from app import socketio
from app.models import IPCamera, CameraImage, FileUtils


def encode_image(img):
    return base64.b64encode(img).decode('ascii')


def read_image(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return image_data


def not_found_image(app):
    with app.app_context():
        return os.path.join(app.root_path, 'not-found-icon.jpg')


enabled = True


def is_enabled():
    global enabled
    return enabled


def display_images(app, ftp_client):
    global enabled
    with app.app_context():

        while is_enabled():
            time.sleep(1)
            ip_cameras = IPCamera.query.all()
            app.logger.info('display running..')
            images = []
            for cam in ip_cameras:

                # list images from camera
                image_list = ftp_client.ls(cam.name)
                # get last image
                latest_image = FileUtils.get_latest_file(image_list)

                if not latest_image:
                    app.logger.info('image not found for camera id:' + str(cam.id))
                    latest_image = not_found_image(app)
                    image = CameraImage(cam.id, cam.name, encode_image(read_image(latest_image)))
                    images.append(image.to_dict())
                    continue
                app.logger.info('image to send:' + latest_image)
                image_data = ftp_client.download(latest_image)
                # encode image
                encoded_image = encode_image(image_data)
                image = CameraImage(cam.id, cam.name, encoded_image)
                images.append(image.to_dict())
            socketio.emit('camera_stream', images, namespace='/test')
