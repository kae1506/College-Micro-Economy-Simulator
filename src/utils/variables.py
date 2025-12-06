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


# =========================
#        STUDENTS
# =========================
class StudentVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Student"

        self.performance = 0.50
        self.happiness = 0.60
        self.fatigue = 0.30
        self.motivation = 0.55
        self.attendance_rate = 0.75
        self.social_engagement = 0.50
        self.extracurricular_engagement = 0.40

        self.variable_names = [
            "performance",
            "happiness",
            "fatigue",
            "motivation",
            "attendance_rate",
            "social_engagement",
            "extracurricular_engagement"
        ]

        if init:
            self.update_values(init)


# =========================
#       PROFESSORS
# =========================
class ProfessorVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Professor"

        self.teaching_quality = 0.70
        self.morale = 0.60
        self.workload = 0.55
        self.experience = 0.80
        self.job_satisfaction = 0.65

        self.variable_names = [
            "teaching_quality",
            "morale",
            "workload",
            "experience",
            "job_satisfaction"
        ]

        if init:
            self.update_values(init)


# =========================
#          CLUBS
# =========================
class ClubsVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Club"

        self.member_count = 0.40
        self.activity_level = 0.55
        self.popularity = 0.45
        self.funding = 0.40
        self.organizational_skill = 0.55

        self.variable_names = [
            "member_count",
            "activity_level",
            "popularity",
            "funding",
            "organizational_skill"
        ]

        if init:
            self.update_values(init)


# =========================
#          ADMIN
# =========================
class AdministrationVariables(ActorVariables):
    def __init__(self, init=None):
        super().__init__(init)
        self.name = "Admin"

        self.efficiency = 0.60
        self.stress_level = 0.35
        self.communication_skill = 0.65
        self.problem_solving = 0.70
        self.leadership = 0.75

        self.variable_names = [
            "efficiency",
            "stress_level",
            "communication_skill",
            "problem_solving",
            "leadership"
        ]

        if init:
            self.update_values(init)