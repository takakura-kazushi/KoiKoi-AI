import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import torch

from client.agent import CustomAgentBase
from client.client import SocketIOClient
from our_models.koikoinets import load_models

# CustomAgentBase を継承して，
# custom_act()を編集してコイコイAIを実装してください．


class MyAgent(CustomAgentBase):
    def __init__(self):
        super().__init__()
        self.discard_model, self.pick_model, self.koikoi_model = load_models()

    def custom_act(self, observation):
        """盤面情報と取れる行動を受け取って，行動を決定して返す関数．参加者が各自で実装．"""

        # てっちゃんへ やってほしいこと
        # `x` と `action_type` を作る
        # observationをもとにする
        # `x` は torch.Tensor
        # `action_type` は "discard", "pick", "koikoi" のどれか

        if action_type == "discard":
            decided_action = self.discard_model.decide_action(x)
        elif action_type == "pick":
            decided_action = self.pick_model.decide_action(x)
        elif action_type == "koikoi":
            decided_action = self.koikoi_model.decide_action(x)
        else:
            raise NotImplementedError

        return decided_action


if __name__ == "__main__":
    my_agent = MyAgent()  # 参加者が実装したプレイヤーをインスタンス化

    mode = int(
        input(
            "Enter mode (1 for playing against AI, 2 for playing against another client): "
        )
    )
    num_games = int(input("Enter number of games to play: "))
    player_name = input("Enter your player name: ")

    sio_client = SocketIOClient(
        ip="localhost",
        port=5000,
        namespace="/koi-koi",
        agent=my_agent,
        room_id=123,
        player_name=player_name,
        mode=mode,
        num_games=num_games,
    )
    sio_client.run()
    # sio.client.enter_room()
