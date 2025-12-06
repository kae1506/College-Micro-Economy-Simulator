from .actor import BaseActor
from src.utils.variables import StudentVariables

class Student(BaseActor):
    def __init__(self, actions_init=None):
        super().__init__(actions_init)
        self.name = "Student"

        # self.performance = 0
        # self.happiness = 0
        # self.fatigue = 0
        # self.motivation = 0
        # self.attendance_rate = 0
        # self.social_engagement = 0
        # self.extracurriculur_engagement = 0

        self.variables = StudentVariables()

        self.actions = [
            "attend_class",
            "study_extra",
            "rest",
            "socialize",
            "seek_help",
            "skip_day",
            "attend_extracurricular"
        ] if actions_init is None else actions_init