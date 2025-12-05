from .actor import BaseActor
from src.utils.variables import ClubsVariables

class Club(BaseActor):
    def __init__(self, actions_init=None):
        super().__init__(actions_init)
        self.name = "Club"
    

        self.variables = ClubsVariables()



        self.actions = [
            "host_event",
            "recruit_members",
            "plan_activity",
            "collaboration_event",
            "request_funding"
        ] if actions_init is None else actions_init