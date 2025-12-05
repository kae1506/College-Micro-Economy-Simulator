from .actor import BaseActor
from src.utils.variables import AdministrationVariables

class Admin(BaseActor):
    def __init__(self, actions_init=None):
        super().__init__(actions_init)
        self.name = "Admin"
    
        self.variables = AdministrationVariables()


        self.actions = [
            "modify_policy",
            "allocate_budget",
            "launch_initiative",
            "conduct_meeting",
            "resolve_issue"
        ] if actions_init is None else actions_init
