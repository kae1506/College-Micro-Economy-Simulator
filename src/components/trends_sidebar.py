# src/components/trends_sidebar.py
from collections import Counter
import streamlit as st


def most_common_action(world, key):
    # actions = [
    #     getattr(a, "latest_action", None)
    #     for a in actors
    #     if getattr(a, "latest_action", None)
    # ]

    # if not actions:
    #     return "—"

    # return Counter(actions).most_common(1)[0][0]
    return world.get_most_common_action(key)


def most_changed_variable(history, prefix):
    """
    Finds which variable (matching prefix) changed the most in absolute terms
    between the previous and latest timestep.
    """
    max_change = 0
    max_var = "—"

    for key, values in history.items():
        if not key.startswith(prefix):
            continue

        if not isinstance(values, list) or len(values) < 2:
            continue

        start = values[-2]
        end = values[-1]

        # Skip weird/nested data
        if isinstance(start, list) or isinstance(end, list):
            continue

        try:
            change = abs(end - start)
        except TypeError:
            continue

        if change > max_change:
            max_change = change
            max_var = key

    return max_var


def render_trends_panel(world):
    st.markdown("### Emergent Trends")

    with st.container(border=True):
        st.markdown("#### Most Common Action")

        st.write("Students:", most_common_action(world, "students"))
        st.write("Professors:", most_common_action(world, "professors"))
        st.write("Clubs:", most_common_action(world, "clubs"))
        st.write("Admins:", most_common_action(world, "admins"))

    st.markdown("---")

    with st.container(border=True):
        st.markdown("#### Most Changed Variable")
        history = world.get_history()

        st.write("Students:", most_changed_variable(history, "stu_"))
        st.write("Professors:", most_changed_variable(history, "prof_"))
        st.write("Clubs:", most_changed_variable(history, "club_"))
        st.write("Admins:", most_changed_variable(history, "admin_"))
