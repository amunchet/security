#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import getopt
import os
import sys
from shutil import move
from subprocess import check_output

from app.models import IPCamera
from displayserverbackend import app


# Script to backup the camera images
# Two functions:
# 1. filemanagement.py -c -d <data directory>
# create empty camera directories if they don't exist

# 2. filemanagement.py -d <data directory>
# backup the camera directories


def create_dirs(data_dir):
    # fetch cameras from db
    with app.app_context():
        ip_cameras = IPCamera.query.all()
        # create camera folders
        print('ip_cameras:', ip_cameras)
        for c in ip_cameras:
            camera_dir_path = os.path.join(data_dir, c.name)
            if not os.path.exists(camera_dir_path):
                print('creating folder:', camera_dir_path)
                os.mkdir(camera_dir_path)


def get_dst(data_dir, timestamp):
    # create folder with time : date +%m.%d.%Y.%H.%M
    dst_basename = timestamp + '.00'
    return os.path.join(data_dir, dst_basename)


def move_dirs(src, dst):
    # move all camera_* to dst
    for file in os.listdir(src):
        camera_dir_path = os.path.join(src, file)
        if os.path.isdir(camera_dir_path) and file.startswith('camera_'):
            move(camera_dir_path, dst)


def create_dirs_and_exit(data_dir):
    create_dirs(data_dir)
    sys.exit()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "cd:")
    except getopt.GetoptError:
        sys.exit(2)
    data_dir = ""
    create_initial_dirs = False
    for opt, arg in opts:
        if opt == "-c":
            create_initial_dirs = True
        elif opt == "-d":
            data_dir = arg

    if not data_dir:
        print('data directory not provided')
        sys.exit(2)
    if create_initial_dirs:
        print('checking if there are missing folders to create and exit')
        create_dirs_and_exit(data_dir)

    timestamp = check_output(["date", "+%m.%d.%Y.%H.%M"], universal_newlines=True).rstrip()
    dst = get_dst(data_dir, timestamp)
    os.mkdir(dst)
    move_dirs(data_dir, dst)
    create_dirs(data_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
