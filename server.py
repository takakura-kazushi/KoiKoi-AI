from __future__ import annotations

import threading
import time
import os
import eventlet
import socketio
from datetime import datetime
import json
import random

class SocketInterface(socketio.Namespace):
    def on_connect(self, sid, environ):
        print('接続しました')
    def on_disconnect(self, sid):
        print('切断されました')
    def on_client_to_server(self, sid, msg):
        print(msg + '受信しました')
        self.emit('response', msg)

class ThreadServer:
    def __init__(self, namespace):
        self.sio_         = socketio.Server(async_mode='eventlet')
        self.app_         = socketio.WSGIApp(self.sio_)
        self.Namespace    = SocketInterface(namespace)
        self.sio_.register_namespace(self.Namespace)
    def start(self):
        eventlet.wsgi.server(eventlet.listen(('localhost', 8000)), self.app_)
    def run(self):
        p = threading.Thread(target=self.start)
        p.setDaemon(True)
        p.start()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    thread_server = ThreadServer('/test')
    thread_server.run()
    while True:
        time.sleep(5)
    #ctr+Cが入力されたら終了
    exit()