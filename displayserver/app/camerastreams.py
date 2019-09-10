#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import os
import time

from app.models import IPCamera, ImageCounter

enabled = True


def is_enabled():
    global enabled
    return enabled


def camera_streams(app, ftp_client, image_downloader):
    ic = ImageCounter()
    with app.app_context():
        while is_enabled():
            time.sleep(2)
            app.logger.info('sending stream')
            ip_cameras = IPCamera.query.all()
            for cam in ip_cameras:
                if not cam.ftp:
                    # check if remote folder exists
                    if cam.name not in ftp_client.ls():
                        app.logger.warning('Folder ' + cam.name + " not found")
                        continue
                    files = ftp_client.ls(cam.name)
                    image_counter = ic.extract_next(cam.id, files)
                    image_name = ic.build_name(image_counter)

                    remote_file_path = os.path.join(cam.name, image_name)

                    # image_downloader = ImageDownloader(cam.host, cam.port)
                    image_content = image_downloader.get_image(cam.host, cam.port)
                    app.logger.info('uploading file:' + remote_file_path)
                    ftp_client.upload_content(remote_file_path, image_content)
