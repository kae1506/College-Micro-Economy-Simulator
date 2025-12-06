# # frontend code
# # two modes: fixed time step, show final steps
# # or manual: where you can cycle it or have it flow

# import streamlit as st
# from src.components.sidebar_controls import render_sidebar
# from src.components.state_dashboard import render_dashboard
# from src.components.actor_inspector import render_actor_inspector
# from src.components.simulation_controls import render_simulation_controls
# from src.components.trends_sidebar import render_trends_panel

# from src.world import World


# st.markdown("""
# <style>
# /* Match right column to sidebar background */
# .trends-panel {
#     background-color: rgba(240, 242, 246, 1);  /* Streamlit sidebar color */
#     padding: 1.2rem;
#     border-radius: 14px;
#     border: 1px solid rgba(49, 51, 63, 0.15);
#     box-shadow: 0 4px 14px rgba(0,0,0,0.05);
# }
# </style>
# """, unsafe_allow_html=True)


# # Ensure one global World() instance through Streamlit session
# if "world" not in st.session_state:
#     st.session_state.world = World()

# world = st.session_state.world

# # Streamlit Page Config
# st.set_page_config(
#     page_title="College Policy Simulator",
#     layout="wide",
# )

# st.markdown(
#     """
#     <style>
#     .block-container {
#         padding-top: 1.5rem;
#         padding-bottom: 2rem;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.title("College Policy Simulator")

# # SIDEBAR
# policy_updates = render_sidebar(world)

# main_col, trends_col = st.columns([4, 1.6], gap="large")

# with main_col:
#     render_simulation_controls(world, policy_updates)
#     render_dashboard(world)
#     render_actor_inspector(world)
# with trends_col:
#     render_trends_panel(world)

# # MAIN BODY
# app.py
import streamlit as st

from src.world import World  # your backend world class

# Frontend components (adjust paths to match your project)
from src.components.sidebar_controls import render_sidebar
from src.components.actor_inspector import render_actor_inspector
from src.components.simulation_controls import render_simulation_controls
from src.components.state_dashboard import render_dashboard
from src.components.trends_sidebar import render_trends_panel  # or render_trends


# ---- Page config ----
st.set_page_config(
    page_title="Campus Micro-Economy Simulator",
    page_icon="🏫",
    layout="wide",
)

# Optional small CSS tweak
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---- Title ----
st.title(" Campus Micro-Economy Simulator")
st.caption("Tweak policies, run the simulation, and watch the campus evolve over time.")


# ---- World in session_state (backend object) ----
if "world" not in st.session_state:
    st.session_state.world = World()

world = st.session_state.world


# ---- Sidebar (policy controls) ----
policy_updates = render_sidebar(world)  # uses your world, returns dict of policy changes


# MAIN LAYOUT

# ---- Mini Summary Bar ----

st.write("")

# ---- Overview (left) + Controls (right) ----
# col_overview, col_controls = st.columns([2, 1])

# with col_overview:
#     st.subheader("📊 Overview")
#     render_dashboard(world)

# with col_controls:
#     st.subheader("🎮 Controls")
#     render_simulation_controls(world, policy_updates)

render_simulation_controls(world, policy_updates)

render_dashboard(world)

st.write("---")

# ---- Tabs for Actors + Trends ----
tabs = st.tabs(["Trends", "Simulation Data"])

# with tabs[0]:
#     render_actor_inspector(world)

with tabs[0]:
    if world.timestep > 0:
        render_trends_panel(world)


with tabs[1]:
    with st.container(border=True):
        st.markdown("### Simulation Summary")

        timestep = world.get_history().get("timestep", [])
        current_step = timestep[-1] if timestep else 0

        colA, colB, colC, colD, colE = st.columns(5)

        colA.metric("Current Step", current_step)
        colB.metric("Students", len(world.students))
        colC.metric("Teachers", len(world.professors))
        colD.metric("Clubs", len(world.clubs))
        colE.metric("Admins", len(world.admins))



# # ---- Main area: Tabs ----
# tab_overview, tab_actors, tab_trends, tab_controls = st.tabs(
#     ["📊 Overview", "🧍 Actors", "📈 Trends", "🎮 Controls"]
# )

# with tab_overview:
#     # global metrics and high-level graphs
#     render_dashboard(world)

# with tab_actors:
#     # inspect individual actors
#     render_actor_inspector(world)

# with tab_trends:
#     # small analytical panels or detailed line charts
#     render_trends_panel(world)  # or render_trends(world) if you prefer that version

# with tab_controls:
#     # run/reset/save/load the simulation
#     render_simulation_controls(world, policy_updates)
