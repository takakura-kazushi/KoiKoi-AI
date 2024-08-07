import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('サーバーに接続しました')

@sio.event
def disconnect():
    print('サーバーから切断されました')

@sio.on('response')
def on_response(data):
    print('サーバーからの応答:', data)

if __name__ == '__main__':
    sio.connect('http://localhost:8000')
    
    try:
        while True:
            message = input("メッセージを入力してください: ")
            sio.emit('message', message)
            time.sleep(1)
    except KeyboardInterrupt:
        sio.disconnect()