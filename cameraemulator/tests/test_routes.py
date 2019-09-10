#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import pytest

from cameraemulator import app


# only be invoked once per test module
@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    app.config['FTP_SUPPORTED'] = 'false'

    def teardown():
        client.get('/stop')

    with app.test_client() as client:
        # trigger background thread activation
        client.get('/image.jpg')
        yield client

    teardown()


def test_get_file(client):
    response = client.get('/image.jpg')
    assert response.status_code == 200


def test_get_not_existing_file(client):
    response = client.get('/not_existsing_image.jpg')
    assert response.status_code == 404
