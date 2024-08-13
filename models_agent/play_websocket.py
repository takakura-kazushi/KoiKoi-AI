import json
import asyncio
import websockets
from koikoigame import KoiKoiGameState
from base_models.koikoilearn import AgentForTest
# from ..client.agent import 
import torch

async def main():
    your_name = input("Enter your name: ")
    ai_name = 'RL-Point'
    record_path = 'gamerecords_player/'

    game_state = KoiKoiGameState(player_name=[your_name, ai_name], 
                                 record_path=record_path, 
                                 save_record=True)
    
    discard_model = torch.load('model_agent/discard_rl_point.pt', map_location=torch.device('cpu'))
    pick_model = torch.load('model_agent/pick_rl_point.pt', map_location=torch.device('cpu'))
    koikoi_model = torch.load('model_agent/koikoi_rl_point.pt', map_location=torch.device('cpu'))

    ai_agent = AgentForTest(discard_model, pick_model, koikoi_model)

    async with websockets.serve(lambda websocket: game_loop(websocket, game_state, ai_agent), "localhost", 8765):
        await asyncio.Future()  # run forever

async def game_loop(websocket, game_state, ai_agent):
    while True:
        if game_state.game_over:
            await websocket.send(json.dumps({"type": "game_over", "result": game_state.winner}))
            break

        state = game_state.round_state.state
        turn_player = game_state.round_state.turn_player

        observation = {
            "feature_tensor": game_state.feature_tensor.tolist(),
            "action_mask": game_state.round_state.action_mask.tolist(),
            "state": state,
            "turn_player": turn_player
        }

        await websocket.send(json.dumps({"type": "observation", "data": observation}))

        if turn_player == 1:
            action_data = await websocket.recv()
            action = json.loads(action_data)["action"]
        else:
            action = ai_agent.auto_action(game_state)

        game_state.round_state.step(action)

        if state == 'round-over':
            game_state.new_round()

if __name__ == "__main__":
    asyncio.run(main())