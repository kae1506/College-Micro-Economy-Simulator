
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
    page_title="College Micro-Economy Simulator",
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
st.title(" College Micro-Economy Simulator")
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
