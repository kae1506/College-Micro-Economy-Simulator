from collections import Counter
import streamlit as st

def most_common_action(actors):
    actions = [getattr(a, "latest_action", None) for a in actors if getattr(a, "latest_action", None)]
    
    if not actions:

        return "—"

    return Counter(actions).most_common(1)[0][0]


def most_changed_variable(history, prefix):
    """
    Finds which variable (matching prefix) changed the most over time.
    Expects history as:
    history = {
        "timestep": [0,1,2],
        "stu_avg_happiness": [..],
        ...
    }
    """

    if not history or "timestep" not in history:
        print("broken1")
        return "—"

    if len(history["timestep"]) < 1:
        print("broken2")
        return "—"


    max_delta = 0
    most_changed = "—"

    for key, values in history.items():
        if not key.startswith(prefix):
            continue

        # ✅ Must be a list with at least 2 numeric values
        if not isinstance(values, list) or len(values) < 2:
            continue

        try:
            start = values[-2]
            end = values[-1]

            # ✅ If somehow nested lists appear, skip safely
            if isinstance(start, list) or isinstance(end, list):
                continue

            delta = abs(end - start)

            if delta > max_delta:
                max_delta = delta
                most_changed = key.replace(prefix, "").replace("_", " ").title()

        except:
            continue  # ✅ Safety net for any unexpected junk

    return most_changed

def render_trends_panel(world):

    st.markdown("### 📊 Live Trends")

    st.markdown("#### 🔥 Most Common Actions")
    st.write("🎓 Students:", most_common_action(world.students))
    st.write("👨‍🏫 Professors:", most_common_action(world.professors))
    st.write("🎉 Clubs:", most_common_action(world.clubs))
    st.write("🏛️ Admins:", most_common_action(world.admins))

    st.markdown("---")

    st.markdown("#### 📈 Most Changed Variable")
    history = world.get_history()

    st.write("🎓 Students:", most_changed_variable(history, "stu_"))
    st.write("👨‍🏫 Professors:", most_changed_variable(history, "prof_"))
    st.write("🎉 Clubs:", most_changed_variable(history, "club_"))
    st.write("🏛️ Admins:", most_changed_variable(history, "admin_"))

