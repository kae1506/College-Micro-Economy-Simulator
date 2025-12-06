# src/components/sidebar_controls.py
import streamlit as st


def render_sidebar(world):
    st.sidebar.title("Policy Controls")
    st.sidebar.caption("Adjust institution-wide policies and rerun the simulation.")




    policy_updates = {}

    with st.sidebar.expander("Schedule & Breaks", expanded=True):
        policy_updates["class_time"] = st.slider(
            "Class starting time (hour)",
            8,
            12,
            8,
            help="Earlier classes may increase stress but free up afternoons.",
        )

        policy_updates["break_frequency"] = st.slider(
            "Break frequency (days/month)",
            0,
            8,
            5,
            help="More breaks may reduce stress but could impact productivity.",
        )

    with st.sidebar.expander("Assessment Load", expanded=True):
        policy_updates["exam_frequency"] = st.slider(
            "Exam frequency (exams / semester per course)",
            0,
            4,
            2,
            help="Higher frequency can raise stress and effort across the campus.",
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Tip:** Change a setting, then use the controls to run a few steps.")

    return policy_updates
