#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import unittest
from unittest import mock

from app import create_app
from app.configurator import create_camera_emulator
from app.emulator import CameraEmulator


def ftp_nlst_side_effect(*args, **kwargs):
    if len(args) == 0:
        return ["camera_1"]
    elif args[0] == "camera_1":
        return ["image0001.jpg", "image0002.jpg"]


class TestEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.execution_counter = 0

    def tearDown(self):
        self.ctx.pop()

    def single_execution(self):
        if self.execution_counter == 0:
            self.execution_counter += 1
            return True
        return False

    @mock.patch('ftplib.FTP')
    def test_emulator_w_ftp(self, ftp_constructor_mock):
        ftp_mock = ftp_constructor_mock.return_value
        ftp_mock.nlst.return_value = []

        with mock.patch.object(CameraEmulator, 'is_enabled', side_effect=self.single_execution):
            camera_emulator = create_camera_emulator()
            camera_emulator.gen_serve_upload(self.app)

        ftp_constructor_mock.assert_called_with('localhost', 'admin', 'pass')

    @mock.patch('ftplib.FTP')
    def test_emulator_w_ftp_remote_files(self, ftp_constructor_mock):
        ftp_mock = ftp_constructor_mock.return_value
        ftp_mock.nlst.side_effect = ftp_nlst_side_effect

        with mock.patch.object(CameraEmulator, 'is_enabled', side_effect=self.single_execution):
            camera_emulator = create_camera_emulator()
            camera_emulator.gen_serve_upload(self.app)
        ftp_constructor_mock.assert_called_with('localhost', 'admin', 'pass')
