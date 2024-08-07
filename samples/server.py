import eventlet
import socketio

sio = socketio.Server(async_mode='eventlet')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('クライアントが接続しました:', sid)

@sio.event
def disconnect(sid):
    print('クライアントが切断しました:', sid)

@sio.on('message')
def handle_message(sid, data):
    print('受信したメッセージ:', data)
    sio.emit('response', 'サーバーからの応答: ' + data, room=sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8000)), app)