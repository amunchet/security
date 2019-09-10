#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import collections
import ftplib
import os
import tempfile
import time


class ImageGenerator:
    def __init__(self, frequency, base_path):
        self.frequency = frequency
        self.offset = 0
        self.base_path = base_path

    # generate and image and
    # returns its path
    def generate(self):
        time.sleep(self.frequency)
        entries = os.listdir(self.base_path)
        if self.offset == len(entries):
            self.offset = 0
        image_path = os.path.join(self.base_path, entries[self.offset])
        self.offset += 1
        return image_path


# get remote files
# upload file
# download file
class FtpClient:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.ftp = ftplib.FTP(self.host, self.user, self.password)

    def ls(self, remote_dir=None):
        if not remote_dir:
            return self.ftp.nlst()
        return self.ftp.nlst(remote_dir)

    def upload_content(self, remote_file_path, content):
        with tempfile.TemporaryFile() as file:
            file.write(content)
            file.seek(0)
            self.ftp.storbinary('STOR ' + remote_file_path, file)

    def upload_file(self, remote_file_path, image_file):
        with open(image_file, 'rb') as file:
            self.ftp.storbinary('STOR ' + remote_file_path, file)

    def download(self, remote_file_path):
        binary = []

        def store_binary(data):
            binary.append(data)

        self.ftp.retrbinary("RETR " + remote_file_path, callback=store_binary)
        return b"".join(binary)


class ImageCounter:
    def __init__(self):
        self.image_counters = collections.defaultdict(int)

    def next(self, cam_id):
        self.image_counters[cam_id] += 1
        return self.image_counters[cam_id]

    def exists(self, cam_id):
        return cam_id in self.image_counters

    def get(self, cam_id):
        return self.image_counters[cam_id]

    def add(self, cam_id, counter=0):
        if counter < 0:
            raise ValueError("counter is negative")
        self.image_counters[cam_id] = counter

    @staticmethod
    def parse(filename):
        basename = os.path.basename(filename)
        filename_wo_extension, _ = os.path.splitext(basename)
        return int(filename_wo_extension.replace('image', ''))

    @staticmethod
    def build_name(counter):
        return 'image' + ImageCounter._add_trailing_zeros(counter) + '.jpg'

    @staticmethod
    def _add_trailing_zeros(counter):
        counter_str = str(counter)
        return counter_str.zfill(4)

    def extract_next(self, cam_id, files):
        if not files:
            self.add(cam_id)
        elif not self.exists(cam_id):
            filename = FileUtils.get_latest_file(files)
            image_counter = self.parse(filename)
            self.add(cam_id, image_counter)
        return self.next(cam_id)


class FileUtils:
    @staticmethod
    def get_latest_file(files):
        if not files:
            return None
        return files[0] if len(files) == 1 else sorted(files)[-1]
