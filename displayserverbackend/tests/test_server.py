#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import unittest
from unittest import mock

from app import create_app, socketio, db, camerastreams, display, routes
from app.models import IPCamera, ImageDownloader, FtpClient


def ftp_nlst_side_effect(*args, **kwargs):
    if len(args) == 0:
        return ["camera_1"]
    elif args[0] == "camera_1":
        return ["image0001.jpg", "image0002.jpg"]


class TestRoutes(unittest.TestCase):
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
        camerastreams.enabled = True
        display.enabled = True

        db.drop_all()
        db.create_all()

    def tearDown(self):
        camerastreams.enabled = False
        display.enabled = False
        routes.camera_streams_thread = None
        routes.display_thread = None
        db.drop_all()
        self.ctx.pop()

    def single_execution(self):
        if self.execution_counter == 0:
            self.execution_counter += 1
            return True
        return False

    @mock.patch('ftplib.FTP')
    @mock.patch.object(ImageDownloader, "get_image", return_value=b'a binary image')
    def test_camera_stream(self, mock_get, ftp_constructor_mock):
        self._init_db()

        ftp_client = FtpClient("localhost", "admin", "pass")
        image_downloader = ImageDownloader()
        mock_ftp = ftp_constructor_mock.return_value
        mock_ftp.nlst.return_value = []
        with mock.patch('app.camerastreams.is_enabled', side_effect=self.single_execution):
            camerastreams.camera_streams(self.app, ftp_client, image_downloader)

    @mock.patch('ftplib.FTP')
    @mock.patch.object(ImageDownloader, "get_image", return_value=b'a binary image')
    def test_camera_stream_remote_files(self, mock_get, ftp_constructor_mock):
        self._init_db()

        ftp_client = FtpClient("localhost", "admin", "pass")
        image_downloader = ImageDownloader()
        mock_ftp = ftp_constructor_mock.return_value
        mock_ftp.nlst.side_effect = ftp_nlst_side_effect
        with mock.patch('app.camerastreams.is_enabled', side_effect=self.single_execution):
            camerastreams.camera_streams(self.app, ftp_client, image_downloader)

    def test_camerastreams_is_enabled(self):
        assert camerastreams.is_enabled()

    def test_display_is_enabled(self):
        assert display.is_enabled()

    @mock.patch('ftplib.FTP')
    def test_display_image_not_found(self, ftp_constructor_mock):
        self._init_db()

        ftp_client = FtpClient("localhost", "admin", "pass")
        mock_ftp = ftp_constructor_mock.return_value
        mock_ftp.nlst.return_value = []
        with mock.patch('app.display.is_enabled', side_effect=self.single_execution):
            display.display_images(self.app, ftp_client)

    def _init_db(self):
        ipcamera = IPCamera()
        ipcamera.id = 1
        ipcamera.port = 5000
        ipcamera.name = 'camera_1'
        ipcamera.host = 'localhost'
        ipcamera.ftp = False

        db.session.add(ipcamera)
        db.session.commit()

    @mock.patch('ftplib.FTP')
    def test_display(self, ftp_constructor_mock):
        self._init_db()

        ftp_client = FtpClient("localhost", "admin", "pass")
        mock_ftp = ftp_constructor_mock.return_value
        mock_ftp.nlst.return_value = ["image0001.jpg", "image0002.jpg"]
        with mock.patch('app.display.is_enabled', side_effect=self.single_execution):
            display.display_images(self.app, ftp_client)
        ftp_constructor_mock.assert_called_with('localhost', 'admin', 'pass')

    @mock.patch('app.display.is_enabled', return_value=False)
    @mock.patch('app.camerastreams.is_enabled', return_value=False)
    @mock.patch('ftplib.FTP')
    def test_connect(self, ftp_constructor_mock, c_enable_mock, d_enable_mock):
        client = socketio.test_client(self.app, namespace='/test')

        self.assertTrue(client.is_connected())

        client.get_received('/test')
        client.emit('my_event', {'data': 'test data'}, namespace='/test')
        received = client.get_received('/test')
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'][0]['data'], 'test data')

        client.get_received('/test')
        client.emit('my_ping', namespace='/test')
        received = client.get_received('/test')
        self.assertEqual(len(received), 1)

        client.disconnect()
        self.assertFalse(client.is_connected())
