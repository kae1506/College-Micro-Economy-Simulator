# src/components/state_dashboard.py
import streamlit as st
import plotly.express as px
import pandas as pd


def render_dashboard(world):
    st.subheader("📊 Global State Overview")

    history = world.get_history()
    groups = world.get_grouped_history()

    # If no timestep → do not render charts
    if len(history.get("timestep", [])) == 0:
        st.info("Run the simulation first to see data.")
        return

    # ============================
    #   GLOBAL STATE METRICS
    # ============================
    with st.container(border=True):
        st.markdown("### Global Environment Metrics")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.metric("Institution reputation", f"{world.env.institution_reputation:.2f}")
        col2.metric("Ambient stress", f"{world.env.ambient_stress_level:.2f}")
        col3.metric("Policy satisfaction", f"{world.env.average_policy_satisfaction:.2f}")
        col4.metric("Class load", f"{world.env.class_load:.2f}")
        col5.metric("Campus energy", f"{world.env.campus_energy:.2f}")
        col6.metric("Break frequency", f"{world.env.class_load:.2f}")  # same as your original

    st.write("---")

    # ============================
    #    ACTOR TREND GRAPHS
    # ============================

    st.subheader("Simulation trends by actor type")
    st.caption("Each panel shows the time-series of key variables for that actor group.")

    timesteps = history["timestep"]

    def create_group_plot(title, vars_list):
        fig = px.line(title=title, template="plotly_white")

        for var in vars_list:
            if var not in history:
                continue
            fig.add_scatter(
                x=timesteps,
                y=history[var],
                mode="lines",
                name=var.replace("_", " ").title(),
            )

        fig.update_layout(
            xaxis_title="Timestep",
            yaxis_title="Value",
            legend_title="Variables",
            height=360,
            margin=dict(l=10, r=10, t=40, b=10),
        )
        return fig

    grid = st.columns(2)
    actor_order = ["Students", "Professors", "Clubs", "Admins"]

    for idx, actor_group in enumerate(actor_order):
        with grid[idx % 2]:
            st.markdown(f"#### {actor_group}")
            vars_list = groups.get(actor_group, [])

            if not vars_list:
                st.info("No variables logged for this actor yet.")
                continue

            fig = create_group_plot(actor_group, vars_list)
            st.plotly_chart(fig, use_container_width=True)
