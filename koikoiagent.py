
from koikoigame import KoiKoiGameState
import numpy as np
import random


class Agent():
    def __init__(self):
        pass 
    
    def auto_random_action(self, game_state):
        action_output = None
        if game_state.round_state.wait_action == True:
            state = game_state.round_state.state
            if state == 'discard':
                turn_player = game_state.round_state.turn_player
                action_output = random.choice(game_state.round_state.hand[turn_player])
            elif state in ['discard-pick', 'draw-pick']:
                action_output = random.choice(game_state.round_state.pairing_card)
            elif state == 'koikoi':
                action_output = random.choice([True, False])
        return action_output 
    
    def __call__(self,game_state):
        return self.auto_random_action(game_state)
    

def get_player_action(game_state):
    round_state = game_state.round_state
    state = round_state.state

    if state == 'discard':
        print("Select a card to discard:")
        for i, card in enumerate(round_state.hand[1]):
            print(f"{i + 1}: {card}")
        while True:
            try:
                choice = int(input("Enter the number of the card: ")) - 1
                if 0 <= choice < len(round_state.hand[1]):
                    return round_state.hand[1][choice]
            except ValueError:
                pass
            print("Invalid choice. Please try again.")

    elif state == 'discard-pick' or state == 'draw-pick':
        if round_state.wait_action:
            print("Select a card to pair:")
            for i, card in enumerate(round_state.pairing_card):
                print(f"{i + 1}: {card}")
            while True:
                try:
                    choice = int(input("Enter the number of the card (or 0 to skip): ")) - 1
                    if choice == -1:
                        return None
                    if 0 <= choice < len(round_state.pairing_card):
                        return round_state.pairing_card[choice]
                except ValueError:
                    pass
                print("Invalid choice. Please try again.")
        return None

    elif state == 'koikoi':
        if round_state.wait_action:
            choice = input("Do you want to Koi-Koi? (y/n): ").lower()
            return choice == 'y'
        return None

    return None

def main():
    your_name = 'AI1'
    ai_name = 'AI2'
    
    game_state = KoiKoiGameState(player_name=[your_name, ai_name])
    
    ai_agent = Agent()
    ai_agent2 = Agent()
    
    while True:
        state = game_state.round_state.state
        turn_player = game_state.round_state.turn_player

        if game_state.game_over:
            print("Game Over!")
            print(f"Final Score: {game_state.player_name[1]}: {game_state.point[1]}, {game_state.player_name[2]}: {game_state.point[2]}")
            break

        elif state == 'round-over':
            print("Round Over!")
            print(f"Round Score: {game_state.player_name[1]}: {game_state.round_state.round_point[1]}, {game_state.player_name[2]}: {game_state.round_state.round_point[2]}")
            game_state.new_round()
            # print_game_status(game_state)

        else:

            if turn_player == 1:
                print("Your turn!")
                action = ai_agent(game_state)
            else:
                print("AI's turn...")
                action = ai_agent2(game_state)

            if state == 'discard':
                game_state.round_state.discard(action)
            elif state == 'discard-pick':
                game_state.round_state.discard_pick(action)
            elif state == 'draw':
                game_state.round_state.draw(action)
            elif state == 'draw-pick':
                game_state.round_state.draw_pick(action)
            elif state == 'koikoi':
                game_state.round_state.claim_koikoi(action)

            print(f"Action taken: {state} - {action}")
        input("continue")

if __name__ == '__main__':
    main()
    
    