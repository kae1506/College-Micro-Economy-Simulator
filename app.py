# frontend code
# two modes: fixed time step, show final steps
# or manual: where you can cycle it or have it flow

import streamlit as st
from src.components.sidebar_controls import render_sidebar
from src.components.state_dashboard import render_dashboard
from src.components.actor_inspector import render_actor_inspector
from src.components.simulation_controls import render_simulation_controls
from src.components.trends_sidebar import render_trends_panel

from src.world import World


st.markdown("""
<style>
/* Match right column to sidebar background */
.trends-panel {
    background-color: rgba(240, 242, 246, 1);  /* Streamlit sidebar color */
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid rgba(49, 51, 63, 0.15);
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)


# Ensure one global World() instance through Streamlit session
if "world" not in st.session_state:
    st.session_state.world = World()

world = st.session_state.world

# Streamlit Page Config
st.set_page_config(
    page_title="College Policy Simulator",
    layout="wide",
)

st.title("College Policy Simulator")

# SIDEBAR
policy_updates = render_sidebar(world)

main_col, trends_col = st.columns([4, 1.6], gap="large")

with main_col:
    render_simulation_controls(world, policy_updates)
    render_dashboard(world)
    render_actor_inspector(world)
with trends_col:
    render_trends_panel(world)

# MAIN BODY
