#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

from threading import Lock

from flask import request, session, current_app
from flask_socketio import emit

from app import socketio
from app.camerastreams import camera_streams
from app.display import display_images
from app.models import FtpClient, ImageDownloader

thread_lock = Lock()
camera_streams_thread = None
display_thread = None


# Counts the events sent by the client
# if a client sends multiple event, the receive count increases
@socketio.on('my_event', namespace='/test')
def test_message(message):
    current_app.logger.info(message['data'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('server_event', {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    pass
    emit('my_pong')


# when a client disconnect (close tab in the browser)
# the server prints the id of the client
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    current_app.logger.info('Client disconnected: ' + request.sid)


# When a client connects, the server sends a Connected message to the client
# Sends the graph if not null
# Then starts a background thread
@socketio.on('connect', namespace='/test')
def client_connect():
    global camera_streams_thread
    global display_thread

    host = current_app.config['FTP_HOST']
    user = current_app.config['FTP_USER']
    password = current_app.config['FTP_PASSWORD']

    with thread_lock:
        if display_thread is None:
            ftp_client = FtpClient(host, user, password)
            display_thread = socketio.start_background_task(display_images, current_app._get_current_object(),
                                                            ftp_client)
        if camera_streams_thread is None:
            ftp_client = FtpClient(host, user, password)
            image_downloader = ImageDownloader()
            camera_streams_thread = socketio.start_background_task(camera_streams, current_app._get_current_object(),
                                                                   ftp_client, image_downloader)

    emit('server_event', {'data': 'Client connected', 'count': 0})
