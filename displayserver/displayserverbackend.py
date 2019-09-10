#  Created by Marcello Monachesi at 9/6/19, 5:39 PM

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=10001)
