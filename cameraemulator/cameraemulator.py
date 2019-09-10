#  Created by Marcello Monachesi at 9/6/19, 5:37 PM

import sys
import threading
import time
import urllib.request

from app import create_app


def start_runner(port):
    def start_loop():
        not_started = True
        counter = 0
        while not_started:
            time.sleep(2)
            try:
                response = urllib.request.urlopen('http://0.0.0.0:' + str(port) + '/image.jpg')
                response.read()
                not_started = False
            except:
                print('Server not yet started')
                counter += 1
                if counter == 3:
                    sys.exit()

    thread = threading.Thread(target=start_loop)
    thread.start()


app = create_app()

if __name__ == '__main__':
    app_port = app.config['PORT']
    start_runner(app_port)
    app.run(host='0.0.0.0', port=app_port)
