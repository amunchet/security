#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import os
from shutil import copyfile
from threading import Thread

from app.models import ImageCounter


class CameraEmulator:
    def __init__(self, name, image_generator, generated_image_path):
        self.camera_name = name
        self.gen_image_path = generated_image_path
        self.image_generator = image_generator
        self.thread = None
        self.enabled = True
        self.ftp_client = None

    def start(self, app):
        if not self.thread:
            thread = Thread(target=self.gen_serve_upload, args=(app,))
            thread.start()

    def stop_camera(self):
        self.enabled = False

    def serve(self, file_path):
        dest = os.path.join(self.gen_image_path, 'image.jpg')
        copyfile(file_path, dest)

    def set_ftp_client(self, ftp_client):
        self.ftp_client = ftp_client

    def is_ftp_supported(self):
        return self.ftp_client is not None

    def is_enabled(self):
        return self.enabled

    def gen_serve_upload(self, app):
        # it bounds the life of the thread to the life of the flask app
        with app.app_context():
            ic = ImageCounter()
            while self.is_enabled():
                file_path = self.image_generator.generate()
                app.logger.info('serving')
                self.serve(file_path)
                if self.is_ftp_supported():

                    # check if remote folder exists
                    if self.camera_name not in self.ftp_client.ls():
                        app.logger.warning('Folder ' + self.camera_name + " not found")
                        continue
                    files = self.ftp_client.ls(self.camera_name)
                    image_counter = ic.extract_next(1, files)

                    image_name = ic.build_name(image_counter)

                    remote_file_path = os.path.join(self.camera_name, image_name)

                    self.ftp_client.upload_file(remote_file_path, file_path)
