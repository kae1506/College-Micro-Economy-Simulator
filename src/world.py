        
from src.actors.student import Student
from src.actors.professors import Professor
from src.actors.clubs import Club
from src.actors.administration import Admin

import json
from src.llm_wrappers import change_variables, action_and_change
import streamlit as st


# ---------- OVERLAY + SPINNER ----------
def show_loading_overlay():
    overlay = st.empty()

    overlay.markdown("""
        <style>
        /* Dark background overlay */
        .overlay-dark {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.6);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>

        <div class="overlay-dark">
            <div class="loader"></div>
        </div>

        <style>
        /* Spinner CSS */
        .loader {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)

    return overlay


class World:
    def __init__(self):

        # ----- GLOBAL ENVIRONMENT STATE -----
        self.env = type("Env", (), {})()

        # TODO: refactor to have variables class
        self.env.class_load = 0.2
        self.env.campus_energy = 0.2
        self.env.average_policy_satisfaction = 0
        self.env.ambient_stress_level = 0
        self.env.institution_reputation = 0

        self.env.variables = [
            "class_load",
            "campus_energy",
            "average_policy_satisfaction",
            "ambient_stress_level",
            "institution_reputation"
        ]


        self.original_policy = {
            "class_time" : 8,
            "break_frequency": 5,
            "exam_frequency": 1
        }

        # ----- ACTORS -----
        self.students = [Student() for _ in range(10)]
        self.professors = [Professor() for _ in range(3)]
        self.clubs = [Club() for _ in range(4)]
        self.admins = [Admin()]

        self.actors = [*self.students, *self.professors, *self.clubs, *self.admins]

        # ----- HISTORY (NO PANDAS) -----
        # TODO: automate this via variables
        self.history = {
            "timestep": [],
        }

        for name in self.students[0].variables.variable_names:
            self.history[f"stu_{name}"] = []

        for name in self.professors[0].variables.variable_names:
            self.history[f"prof_{name}"] = []

        for name in self.clubs[0].variables.variable_names:
            self.history[f"club_{name}"] = []

        for name in self.admins[0].variables.variable_names:
            self.history[f"admin_{name}"] = []

        self.timestep = 0


        # self.load_data("run1_class11_break4_exam4")


    # ----------------------------
    # Helper: safe averaging
    # ----------------------------
    @staticmethod
    def safe_avg(values):
        values = [v for v in values if isinstance(v, (int, float))]
        return sum(values) / len(values) if values else 0
    

    def get_most_common_action(self, key):
        return self.history["dominant_actions"][key]
    

    def package_variables(self, glob=True, actor=True):
        ## packages variable averages and global variables


        student_data = ""
        data = {}
        if actor:
            student_data += "Actor Data: "


            for name in self.students[0].variables.variable_names:

                data[f"stu_{name}"] = [] 
            for student in self.students:
                for name in student.variables.variable_names:
                    data[f"stu_{name}"].append(getattr(student.variables, name))
            

            for name in self.professors[0].variables.variable_names:
                data[f"prof_{name}"] = [] 
            for professor in self.professors:
                for name in professor.variables.variable_names:
                    data[f"prof_{name}"].append(getattr(professor.variables, name))
            
        
            for name in self.clubs[0].variables.variable_names:
                data[f"club_{name}"] = [] 
            for club in self.clubs:
                for name in club.variables.variable_names:
                    data[f"club_{name}"].append(getattr(club.variables, name))
            
            for name in self.admins[0].variables.variable_names:
                data[f"admin_{name}"] = [] 
            for admin in self.admins:
                for name in admin.variables.variable_names:
                    data[f"admin_{name}"].append(getattr(admin.variables, name))


            for key in data:
                student_data += f"{key} : {self.safe_avg(data[key])}, "
        
        if glob:
            for name in self.env.variables:
                student_data += f" {name} : {getattr(self.env, name)}"


        return student_data
    


    def current_actors_variables(self, avg=False):
        # TODO: integrate avg or not and combine both functions.


        data = "Actors Variables: "
        for i, student in enumerate(self.students):
            data += f"Student {i+1}: "
            for name in student.variables.variable_names:
                data += f"{name}: {getattr(student.variables, name)}"

        for i, professor in enumerate(self.professors):
            data += f"Professor {i+1}: "
            for name in professor.variables.variable_names:
                data += f"{name}: {getattr(professor.variables, name)}"

        for i, club in enumerate(self.clubs):
            data += f"Club {i+1}: "
            for name in club.variables.variable_names:
                data += f"{name}: {getattr(club.variables, name)}"


        for i, admin in enumerate(self.admins):
            data += f"Admin {i+1}: "
            for name in admin.variables.variable_names:
                data += f"{name}: {getattr(admin.variables, name)}"

        return data


    # ----------------------------  
    # STEP FUNCTION
    # ----------------------------
    def step(self, policy_updates):
        query = "policies have moved from: "
        for key in self.original_policy:
            query+=f'{key}: {self.original_policy[key]}'
        query += ' , to: '
        for key in policy_updates:
            query+=f'{key}: {policy_updates[key]}'
        self.timestep += 1


        ########## FLOW OF STEP: ############
        # FIRST THE VARIABLES ARE AVERAGED AND PACKAGED AND SENT TO UPDATE GLOBAL VARIABLES
        # THEN WITH UPDATED GLOBAL VARIABLES (AND MAYBE AVERAGES OF ALL) ACTORS MAKE ACTIONS
        # THESE ACTIONS THEN UPDATE ACTORS AND GLOBAL VARIABLES. 

        # 1. define function to package variables together
        student_data = self.package_variables()

        overlay = show_loading_overlay()


        # 2. get updated global variables and update (done in func)
        changed = change_variables(query, student_data, self.env)

        # 3. have actors take decision based on global actions and update values
        global_changed = self.package_variables(actor=False)
        current_actors = self.current_actors_variables(avg=False)
        action_and_change(query, global_changed, current_actors, self.actors)


        overlay.empty()



        ## want to have one query taking action+changing for each type of actor
        ## want to get current variables packaged, (not averaged)
        ## then ask model to give answers in the form

        ##############################################################################################
        # === LOGGING (NO PANDAS) ===
        self.history["timestep"].append(self.timestep)


        for name in self.students[0].variables.variable_names:
            self.history[f"stu_{name}"].append(self.safe_avg([getattr(s.variables, name) for s in self.students]))



        for name in self.professors[0].variables.variable_names:
            self.history[f"prof_{name}"].append(self.safe_avg([getattr(s.variables, name) for s in self.professors]))

        for name in self.clubs[0].variables.variable_names:
            self.history[f"club_{name}"].append(self.safe_avg([getattr(s.variables, name) for s in self.clubs]))

        for name in self.admins[0].variables.variable_names:
            self.history[f"admin_{name}"].append(self.safe_avg([getattr(s.variables, name) for s in self.admins]))

    

    def save_data(self, name):
        with open(f"/Users/keshava/Documents/micro-economy-simulator/data/{name}.json", "w") as file:
            json.dump(self.history, file, indent=4)

    def load_data(self, name):
        with open(f'/Users/keshava/Documents/micro-economy-simulator/data/{name}', 'r') as file:
            self.history = json.load(file)

        self.timestep = self.history["timestep"][-1]
        # st.session_state["class_time"] = self.history["policy"]["class_time"]
        # st.session_state["break_frequency"] = self.history["policy"]["break_frequency"]
        # st.session_state["exam_frequency"] = self.history["policy"]["exam_frequency"]
        # st.rerun()

        self.env.campus_energy = self.history["campus_energy"][-1]
        self.env.average_policy_satisfaction = self.history["average_policy_satisfaction"][-1]
        self.env.ambient_stress_level = self.history["ambient_stress_level"][-1]
        self.env.institution_reputation = self.history["institution_reputation"][-1]
    # Streamlit accessors
    # ----------------------------
    def get_history(self):
        """Returns the raw dict history (plot directly)."""
        return self.history
    
    def get_actors_of_type(self, name):
        name = name.lower() + 's'
        return getattr(self, name)

    def get_grouped_history(self):
        """
        Automatically groups actor-based history metrics.
        Returns dictionary like:
        {
            "Students": ["stu_avg_happiness", "stu_avg_fatigue", ...],
            "Professors": [...],
            "Clubs": [...],
            "Admins": [...],
        }
        """
        groups = {
            "Students": [],
            "Professors": [],
            "Clubs": [],
            "Admins": []
        }

        for key in self.history.keys():
            if key.startswith("stu_"):
                groups["Students"].append(key)
            elif key.startswith("prof_"):
                groups["Professors"].append(key)
            elif key.startswith("club_"):
                groups["Clubs"].append(key)
            elif key.startswith("admin_"):
                groups["Admins"].append(key)

        return groups