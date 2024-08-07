# import time
# import eventlet
# import socketio
# import json
# import random

# from datetime import datetime

# from __future__ import annotations

# # SocketIOのテンプレート
# class SocketIOClient:
#     # 初期化
#     def __init__(self,ip,port,namespace,query,agent,room_id,player_name):
#         # self.ip_         = ip
#         # self.port_       = port
#         # self.namespace_  = namespace
#         # self.query_      = query
#         # self.is_connect_ = False
#         self.sio_        = socketio.Client()
#         # self.Namespace   = self.NamespaceClass(self.namespace_)
#         # self.overload_event()
#         # self.sio_.register_namespace(self.Namespace)
#         # self.agent = agent
#         # self.room_id = room_id
#         # self.player_name = player_name
#     # サーバーから切断された場合の処理
#         @sio.event
#         def disconnect():
#             print('サーバーから切断されました')
        
#         # サーバーからメッセージを受信した場合の処理
#         @sio.event
#         def message(data):
#             print(f'サーバーからのメッセージ: {data}')
            
#         def on_message(self, data):
#             print('Received message %s', str(data))
#     # サーバーからイベント名「server_to_client」でデータがemitされた時に呼ばれる
#         def on_server_to_client(self, data):
#             print('Received message %s', str(data))
# if __name__ == '__main__':
#     # Ctrl + C (SIGINT) で終了
#     # signal.signal(signal.SIGINT, signal.SIG_DFL)
#     # SocketIO Client インスタンスを生成
#     agent = agents.ShantenAgent()
#     room_id = 123  # NOTE: DEBUG
#     sio_client = SocketIOClient('localhost', 5000, '/test', 'secret', agent, room_id)
#     # SocketIO Client インスタンスを実行
#     sio_client.run()
#     sio_client.enter_room()

import socketio
import json
import torch
from koikoigame import KoiKoiGameState
from koikoilearn import AgentForTest

class KoiKoiClient(socketio.ClientNamespace):
    def __init__(self, namespace, agent, your_name='Player', ai_name='RL-Point', record_path='gamerecords_player/'):
        super().__init__(namespace)
        self.agent = agent
        self.your_name = your_name
        self.ai_name = ai_name
        self.record_path = record_path
        self.setup_game()

    def setup_game(self):
        record_fold = self.record_path + self.ai_name + '/'
        for path in [self.record_path, record_fold]:
            if not os.path.isdir(path):
                os.mkdir(path)

        if self.ai_name == 'SL':
            discard_model_path = 'model_agent/discard_sl.pt'
            pick_model_path = 'model_agent/pick_sl.pt'
            koikoi_model_path = 'model_agent/koikoi_sl.pt'
        elif self.ai_name == 'RL-Point':
            discard_model_path = 'model_agent/discard_rl_point.pt'
            pick_model_path = 'model_agent/pick_rl_point.pt'
            koikoi_model_path = 'model_agent/koikoi_rl_point.pt'
        elif self.ai_name == 'RL-WP':
            discard_model_path = 'model_agent/discard_rl_wp.pt'
            pick_model_path = 'model_agent/pick_rl_wp.pt'
            koikoi_model_path = 'model_agent/koikoi_rl_wp.pt'

        self.game_state = KoiKoiGameState(player_name=[self.your_name, self.ai_name], record_path=record_fold, save_record=True)
        self.discard_model = torch.load(discard_model_path, map_location=torch.device('cpu'))
        self.pick_model = torch.load(pick_model_path, map_location=torch.device('cpu'))
        self.koikoi_model = torch.load(koikoi_model_path, map_location=torch.device('cpu'))
        self.ai_agent = AgentForTest(self.discard_model, self.pick_model, self.koikoi_model)

    def on_connect(self):
        print('Connected to server')
        self.emit('join', {'player_name': self.your_name})

    def on_disconnect(self):
        print('Disconnected from server')

    def on_message(self, data):
        print(f'Received message: {data}')

    def on_game_state(self, data):
        self.game_state.load(data)
        action = self.get_player_action()
        self.emit('action', {'player': self.your_name, 'action': action})

    def get_player_action(self):
        state = self.game_state.round_state.state
        turn_player = self.game_state.round_state.turn_player

        if turn_player == 1:
            action = get_player_action(self.game_state)
        else:
            action = self.ai_agent.auto_action(self.game_state)
        return action

def main():
    sio = socketio.Client()
    agent = None  # Your agent instance if needed
    client = KoiKoiClient(namespace='/koikoi', agent=agent)
    sio.register_namespace(client)
    sio.connect('http://localhost:5000')
    sio.wait()

if __name__ == '__main__':
    main()