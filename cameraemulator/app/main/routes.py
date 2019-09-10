#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

from flask import send_file, abort, current_app
from app.main import bp
from app.configurator import create_camera_emulator


camera_emulator = None


@bp.route('/<file_name>')
def get_file(file_name):
    path = 'generated-image/' + file_name
    try:
        return send_file(path, mimetype='image/jpeg')
    except FileNotFoundError:
        abort(404, 'File Not found:' + file_name)


@bp.before_app_request
def start_emulator():
    global camera_emulator
    if not camera_emulator:
        camera_emulator = create_camera_emulator()
        camera_emulator.start(current_app._get_current_object())
        current_app.logger.info("here")


@bp.route('/stop')
def stop_emulator():
    global camera_emulator
    if camera_emulator:
        camera_emulator.stop_camera()
    return ''
