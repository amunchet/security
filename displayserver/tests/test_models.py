#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

import pytest

from app.models import ImageCounter, FileUtils, FtpClient, ImageDownloader


class TestImageCounter:
    def test_next(self):
        image_counter = ImageCounter()
        image_counter.add(1)

        assert image_counter.next(1) == 1

    def test_exists(self):
        image_counter = ImageCounter()
        image_counter.add(1)

        assert image_counter.exists(1)

    def test_get(self):
        image_counter = ImageCounter()
        image_counter.add(1)

        assert image_counter.get(1) == 0

        image_counter.next(1)

        assert image_counter.get(1) == 1

    def test_add(self):
        image_counter = ImageCounter()
        image_counter.add(1)

        assert image_counter.get(1) == 0

        image_counter.add(1, 5)

        assert image_counter.get(1) == 5

    def test_add_negative(self):
        with pytest.raises(ValueError):
            image_counter = ImageCounter()
            image_counter.add(1, -1)

    def test_parse(self):
        file_name = 'image0001.jpg'

        assert ImageCounter.parse(file_name) == 1

    def test_build_name(self):
        counter = 1
        expected = 'image0001.jpg'

        assert ImageCounter.build_name(counter) == expected

    def test_extract_next(self):
        image_counter = ImageCounter()

        files = ['image0001.jpg', 'image0002.jpg', 'image0003.jpg']

        assert image_counter.extract_next(1, files) == 4

    def test_extract_next_empty(self):
        image_counter = ImageCounter()

        files = []

        assert image_counter.extract_next(1, files) == 1


class TestFileUtils:
    def test_get_latest(self):
        files = ['image0001.jpg', 'image0002.jpg', 'image0003.jpg']

        assert FileUtils.get_latest_file(files) == 'image0003.jpg'

    def test_get_latest_from_empty(self):
        files = []

        assert not FileUtils.get_latest_file(files)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

    return MockResponse(b'a little binary image', 200)


class TestImageDownloader:

    def test_get_image(self, mocker):
        requests_mock = mocker.patch('requests.get', side_effect=mocked_requests_get)
        image_downloader = ImageDownloader()
        image_downloader.get_image('localhost', '5000')
        requests_mock.assert_called_once_with("http://localhost:5000/image.jpg")


class TestFtpClient:
    def test_ls(self, mocker):
        ftp_constructor_mock = mocker.patch('ftplib.FTP')
        mock_ftp = ftp_constructor_mock.return_value
        ftp_client = FtpClient('ftp.server.local', 'user', 'pass')
        ftp_client.ls('/remote/path')

        ftp_constructor_mock.assert_called_with('ftp.server.local', 'user', 'pass')
        mock_ftp.nlst.assert_called_with('/remote/path')

    def test_upload_content(self, mocker):
        ftp_constructor_mock = mocker.patch('ftplib.FTP')
        mock_ftp = ftp_constructor_mock.return_value
        ftp_client = FtpClient('ftp.server.local', 'user', 'pass')
        ftp_client.upload_content('/remote/path', b'binary content')

        ftp_constructor_mock.assert_called_with('ftp.server.local', 'user', 'pass')
        mock_ftp.storbinary.assert_called_once()

    def test_upload_file(self, mocker):
        ftp_constructor_mock = mocker.patch('ftplib.FTP')
        mock_ftp = ftp_constructor_mock.return_value
        open_mock = mocker.patch('builtins.open', mocker.mock_open(read_data='bibble'))

        ftp_client = FtpClient('ftp.server.local', 'user', 'pass')
        ftp_client.upload_file('/remote/path', '/local/path')

        open_mock.assert_called_once_with('/local/path', 'rb')
        ftp_constructor_mock.assert_called_with('ftp.server.local', 'user', 'pass')
        mock_ftp.storbinary.assert_called_once()

    def test_download(self, mocker):
        ftp_constructor_mock = mocker.patch('ftplib.FTP')
        mock_ftp = ftp_constructor_mock.return_value
        ftp_client = FtpClient('ftp.server.local', 'user', 'pass')
        ftp_client.download('/remote/path')

        ftp_constructor_mock.assert_called_with('ftp.server.local', 'user', 'pass')
        mock_ftp.retrbinary.assert_called_once()
