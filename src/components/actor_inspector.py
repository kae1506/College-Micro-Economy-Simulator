import streamlit as st

def render_actor_inspector(world):
    st.subheader("Actor Inspector")

    actor_type = st.selectbox("Select Actor Type", ["Student", "Teacher", "Club", "Admin"])

    try:
        actors_list = world.get_actors_of_type(actor_type)
    except:
        st.warning("World class missing get_actors_of_type()")
        return

    index = st.number_input(
        f"Select {actor_type} Index",
        min_value=0,
        max_value=len(actors_list) - 1,
        step=1,
    )

    actor = actors_list[int(index)]

    st.write("### Current State")
    st.json(actor.__dict__)

    if hasattr(actor, "last_action"):
        st.write("### Last Action")
        st.write(actor.last_action)