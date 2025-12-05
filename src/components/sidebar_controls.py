import streamlit as st

def render_sidebar(world):
    st.sidebar.title("Policy Controls")

    policy_updates = {}

    policy_updates["class_time"] = st.sidebar.slider(
        "Class Starting Time", 8, 12, world.original_policy["class_time"]
    )
    policy_updates["break_frequency"] = st.sidebar.slider(
        "Break Frequency (days/month)", 0, 8, world.original_policy["break_frequency"]
    )

    policy_updates["exam_frequency"] = st.sidebar.slider(
        "Exam Frequency (exams/semester) for a course", 0, 4, world.original_policy["exam_frequency"]
    )


    return policy_updates