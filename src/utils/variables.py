class ActorVariables:
    def __init__(self, init=None):
        self.variable_names = []
        if init:
            self.update_values(init)
    
    def dictify(self):
        k = {}
        for name in self.variable_names:
            k[name] = getattr(self, name)
        return k


    def update_values(self, values_new):
        for name in self.variable_names:
            setattr(self, name, values_new)


class StudentVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Student"

        self.performance = 0
        self.happiness = 0
        self.fatigue = 0
        self.motivation = 0
        self.attendance_rate = 0
        self.social_engagement = 0
        self.extracurriculur_engagement = 0

        self.variable_names = ["performance", "happiness", "fatigue", "motivation", "attendance_rate", "social_engagement", "extracurriculur_engagement"]
        if init:
            self.update_values(init)

class ProfessorVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Professor"

        self.teaching_quality = 0
        self.morale = 0
        self.workload = 0
        self.experience = 0
        self.job_satisfaction = 0

        self.variable_names = [
            "teaching_quality",
            "morale",
            "workload",
            "experience",
            "job_satisfaction"
        ]

        if init:
            self.update_values(init)


class ClubsVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Club"

        self.member_count = 0
        self.activity_level = 0
        self.popularity = 0
        self.funding = 0
        self.organizational_skill = 0

        self.variable_names = [
            "member_count",
            "activity_level",
            "popularity",
            "funding",
            "organizational_skill"
        ]

        if init:
            self.update_values(init)


class AdministrationVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Admin"

        self.efficiency = 0
        self.stress_level = 0
        self.communication_skill = 0
        self.problem_solving = 0
        self.leadership = 0

        self.variable_names = [
            "efficiency",
            "stress_level",
            "communication_skill",
            "problem_solving",
            "leadership"
        ]

        if init:
            self.update_values(init)