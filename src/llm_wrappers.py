from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key: 
    print("Error: GEMINI_API_KEY not set in environment.")
    exit()



# api_key = "AIzaSyBOnmWwNt9Sa5qKOxu0IBJSii_onNJowa0"
system_prompt = "you are providing a reward model here. in the input, i will give a policy change taken. " \
"i will give the specific action taken, and the state variables i want to see change in and their initial values." \
"you will then return, in your opinion, how you think those state variables wille be affected NUMERICALLY" \
"do not be verbose. include NO text in the response. just simple return the new values of each state variable" \
"note that the state variables have a range of 0-1. be relative and realistic. it is a college environment." \
"consider all possible changes and possible connections between policy changes and also between state variables" \
"for context, i am providing the list of all state variables and actions. Note that this is meant for a simulation" \
"of a college environment. Be realistic and consistent and use the principles of behavioural economics to inform" \
"your decision. The prompt will come in the form of Policy Change, variable1: value, variable2:value, variable3:value" \
"You will return the prompt in the EXACT format of variable1: new_value, variable2:new_value, ...," \
"" \
"" \
"" \
"" \
"" \
"" \
"" \
"" \
"" \
"" \


system_prompt_actor = "you are providing both the policy and reward model here. in the input i will give the policy change occured, how the" \
"global variable of the environment have been affected, the current variables for each actor, and the available actions for each actor. " \
"in return, you will give the action that each actor will take, and how those actors's variables will be affected, NUMERICALLY." \
"do not return anything other than that. do not update the global variables. only show the actions and the updated actors variables" \
"do not be verbose. include NO text in the response. just simple return the new values of each state variable" \
"note that the variables have a range of 0-1. be relative and realistic. it is a college environment." \
"consider all possible changes and possible connections between policy changes and also between state variables" \
"for context, i am providing the list of all state variables and actions. Note that this is meant for a simulation" \
"of a college environment. Be realistic and consistent and use the principles of behavioural economics to inform" \
"your decision. The prompt will come in the form of variable1: value, variable2:value, variable3:value" \
"You will return the prompt in the EXACT format of actor number, action, variable1:value, variable2:value, ....; actor number, action, " \
"make sure it is in that EXACT format. actor number, action, variable:value... ; actor number, action and so on. do not add " \
"any new line characters. or spaces. make sure you return one row for one actor, and exactly the amount of actors for each actor type." \
"for each actor"

info = (
    "Global State Variables: "
    "class_load, break_frequency, campus_energy, average_policy_satisfaction, "
    "ambient_stress_level, institution_reputation | "

    "Student State Variables: "
    "performance, happiness, fatigue, motivation, attendance_rate, "
    "social_engagement, extracurricular_engagement | "
    "Student Actions: attend_class, study_extra, rest, socialize, seek_help, "
    "skip_day, attend_extracurricular | "

    "Professor State Variables: "
    "teaching_quality, morale, workload, experience, job_satisfaction | "
    "Professor Actions: conduct_lecture, grade_assignments, update_curriculum, "
    "hold_office_hours, attend_training | "

    "Club State Variables: "
    "member_count, activity_level, popularity, funding, organizational_skill | "
    "Club Actions: host_event, recruit_members, plan_activity, "
    "collaboration_event, request_funding | "

    "Admin State Variables: "
    "efficiency, stress_level, communication_skill, problem_solving, leadership | "
    "Admin Actions: modify_policy, allocate_budget, launch_initiative, "
    "conduct_meeting, resolve_issue"
)


system_prompt += info
system_prompt_actor += info


# prompt engineering: we need to engineer prompts in a specfic manner
# for most context, we want to have all the state variables and actions given
# for change in variables due to policy change, we will want to give values for state variables
# and also the average of maybe each variable for each actor. 
# let us try solely for student

client = genai.Client(api_key=api_key)
# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="in a college, all classes are now pushed from 9AM to 10AM in the morning. state variables are: " \
#     "attendance: 0.3, performance: 0.5, extracurriculurs: 0.6",
#     config=types.GenerateContentConfig(
#         system_instruction=system_prompt,
#         temperature=0.9
#     ),
# )

# TODO: ask it to return links
# manually format links and filter them out
# filter out the input structure


def change_variables(query, variables, object_to_update):
    # format variables
    # 


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query+variables,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.9
        ),
    )

    ans = response.text.split(', ')
    ans = [a.split(': ') for a in ans]
    ans_d = {a[0]:float(a[1]) for a in ans}


    for key in ans_d:
        try:
            setattr(object_to_update, key, ans_d[key])
        except:
            pass

    return ans_d


def action_and_change(query, variables, actor_variables, objects):

    # TODO: add current variables for each actor, and possible actions

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query+' '+variables+' '+actor_variables,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt_actor,
            temperature=0.9
        ),
    )


    ans = response.text.strip().split(';')
    ans2 = []
    for x in ans:
        try:
            ans2.append(x.split(','))
        except:
            pass
    actor_nums = [x[0] for x in ans2]
    actions = [x[1] for x in ans2]


    vars = []
    for i, x in enumerate(ans2):
        vars.append([])
        for y in x[2:]:
            try:
                vars[i].append(y.split(':'))
            except:
                pass

    vars2 = []
    for i, x in enumerate(vars):
        vars2.append({})
        for var in x:
            if len(var) == 1:
                var = var[0].split(':')
            
            vars2[i][var[0]] = float(var[1])
    for i in range(len(actor_nums)):
        actor = objects[i]
        actor.take_action(actions[i], vars2[i])




# from src.utils.variables import StudentVariables
# vars = StudentVariables()

# # change_variables("classes move from 9AM to 10AM", vars)

# # design a metric to understand change in environment variable 
# and have it 


