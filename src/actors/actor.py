import random
from src.llm_wrappers import change_variables


class BaseActor:
    def __init__(self, actions_init=None):


        self.actions = [] if actions_init is None else actions_init
        self.actions_history = []
        self.latest_action = "None"


    def take_action(self, action, update):
        """
        implement code to take a specific action based on LLMs
        """

        self.latest_action = action
        self.actions_history.append(action)

        for k in update:
            nk = k.strip()

            setattr(self.variables, nk, update[k])



    
