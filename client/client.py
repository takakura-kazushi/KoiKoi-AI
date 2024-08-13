import socketio
import sys
import os
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),)))
from agent import CustomAgentBase
from abc import ABC, abstractmethod
from tqdm import tqdm
import time

class CustomAgentBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def custom_act(self, observation):
        pass

    def act(self, observation):
        try:
            return self.custom_act(observation)
        except:
            legal_actions = observation['legal_action']
            if len(legal_actions) == 1:
                return legal_actions[0]
            for action in legal_actions:
                if action is None or action is False:
                    return action
            return legal_actions[0]
class SocketIOClient:
    def __init__(self, ip, port, namespace, agent: CustomAgentBase, room_id, player_name, mode, num_games=1):
        self.sio = socketio.Client()
        self.ip = ip
        self.port = port
        self.namespace = namespace
        self.agent = agent
        self.room_id = room_id
        self.player_name = player_name
        self.mode = mode
        self.num_games = num_games
        self.games_played = 0
        self.progress_bar = tqdm(total=num_games, desc="Games Progress", unit="game")
        self.connected = False
        self.connection_established = False
        

        @self.sio.event(namespace=self.namespace)
        def connect():
            print('Connected to server')
            # self.enter_room()
            self.connected = True

        @self.sio.event(namespace=self.namespace)
        def disconnect():
            print('Disconnected from server')

        @self.sio.event(namespace=self.namespace)
        def connection_established():
            print('Connection established, entering room')
            self.connection_established = True
            # self.enter_room()
            
        @self.sio.on('ask_act', namespace=self.namespace)
        def on_ask_act(observation):
            action = self.agent.act(observation)
            self.sio.emit('action', {'room_id': self.room_id, 'action': action}, namespace=self.namespace)

        @self.sio.on('game_over', namespace=self.namespace)
        def on_game_over(data):
            if 'result' in data:
                self.progress_bar.close()
                print(f"Game over. Final results: {data['result']}")
                self.sio.disconnect()
            if 'winner' in data:
                self.games_played += 1
                self.progress_bar.update(1)
                print(f"Winner of this game: Player {data['winner']}")

    def connect(self):
        url = f'http://{self.ip}:{self.port}'
        self.sio.connect(url, namespaces=[self.namespace])

    def enter_room(self):
        if not self.connected:
            print("Not connected to server yet. Waiting...")
            return
        
        data = {
            'room_id': self.room_id,
            'player_name': self.player_name,
            'mode': self.mode,
            'num_games': self.num_games
        }
        print(f"Sending enter_room event with data: {data}")  # デバッグ出力
        self.sio.emit('enter_room', data=data, namespace=self.namespace)

    def run(self):
        self.connect()
        # 接続が確立されるまで待つ
        timeout = 10  # タイムアウト秒数
        start_time = time.time()
        while not (self.connected and self.connection_established):
            time.sleep(0.1)
            if time.time() - start_time > timeout:
                print("Connection timeout")
                return

        print("Entering room...")
        self.enter_room()
        self.sio.wait()
        
if __name__ == '__main__':
    # SocketIO Client インスタンスを生成
    room_id = 123  # NOTE: DEBUG
    sio_client = SocketIOClient('localhost', 5000, '/test', 'secret', agent, room_id)
    