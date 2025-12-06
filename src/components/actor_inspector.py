# src/components/actor_inspector.py
import streamlit as st


def render_actor_inspector(world):
    st.subheader("🧍 Actor Inspector")
    st.caption("Choose an actor and inspect its internal state and recent actions.")

    actor_type = st.selectbox(
        "Actor type",
        ["Student", "Professor", "Club", "Admin"],
    )

    try:
        actors_list = world.get_actors_of_type(actor_type)
    except Exception:
        st.warning("World class is missing `get_actors_of_type()`.")
        return

    if not actors_list:
        st.info(f"No {actor_type.lower()}s present in the world yet.")
        return

    # Show actors as "Student #0", "Student #1", etc. rather than raw index.
    labels = [f"{actor_type} #{i}" for i in range(len(actors_list))]
    selected_label = st.selectbox("Select actor", labels)
    index = labels.index(selected_label)
    actor = actors_list[index]

    with st.container(border=True):
        st.markdown("#### 🧬 Current State")
        st.json(actor.__dict__)

        if hasattr(actor, "last_action"):
            st.markdown("#### 🕒 Last Action")
            st.write(actor.last_action)
