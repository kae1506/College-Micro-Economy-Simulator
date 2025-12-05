from .actor import BaseActor
from src.utils.variables import ProfessorVariables

class Professor(BaseActor):
    def __init__(self, actions_init=None):
        super().__init__(actions_init)
        self.name = "Professor"


        self.variables = ProfessorVariables()

        self.actions = [
            "conduct_lecture",
            "grade_assignments",
            "update_curriculum",
            "hold_office_hours",
            "attend_training"
        ] if actions_init is None else actions_init
