# from abc import abstractmethod
# import KoiKoiGameState 
import koikoigame
# class Agent():
#     def __init__(self):
#         pass 
#     def auto_action(self,observation):
# 	    legalaction = koikoigame.KoiKoiGameState.obeservation.legal_action
#         return random.choice(legal_action)

from abc import abstractmethod

class CustomAgentBase:
    def __init__(self):
        pass

    @abstractmethod
    def custom_act(self, obs):
        pass

    def act(self, observation):
        try:
            return self.custom_act(observation)
        except:
            legal_actions = koikoigame.KoiKoiGameState.obeservation.legal_actions()
            if len(legal_actions) == 1:
                return legal_actions[0]
            for action in legal_actions:
                if action in ['discard', 'pass']:
                    return action

class RandomAgent(CustomAgentBase):
    def custom_act(self, obs):
        import random
        return random.choice(obs.legal_actions())
