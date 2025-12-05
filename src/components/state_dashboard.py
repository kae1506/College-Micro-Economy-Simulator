import streamlit as st
import plotly.express as px
import pandas as pd


def render_dashboard(world):
    st.subheader("Global State Overview")

    history = world.get_history()
    groups = world.get_grouped_history()

    # If no timestep → do not render charts
    if len(history["timestep"]) == 0:
        st.info("Run the simulation first to see data.")
        return

    # ============================
    #   GLOBAL STATE METRICS
    # ============================
    st.write("### Global Environment Metrics")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Institution Reputation", f"{world.env.institution_reputation:.2f}")
    col2.metric("Ambient Stress", f"{world.env.ambient_stress_level:.2f}")
    col3.metric("Policy Satisfaction", f"{world.env.average_policy_satisfaction:.2f}")
    col4.metric("Class Load", f"{world.env.class_load:.2f}")
    col5.metric("Campus Energy", f"{world.env.campus_energy:.2f}")
    col6.metric("Break Frequency", f"{world.env.class_load:.2f}")



    st.write("---")

    # ============================
    #    ACTOR TREND GRAPHS
    # ============================

    st.subheader("Simulation Trends by Actor Type")

    # Helper: create line graph with all vars for a group
    def create_group_plot(title, vars_list):
        fig = px.line(title=title)

        for var in vars_list:
            fig.add_scatter(
                x=history["timestep"],
                y=history[var],
                mode="lines",
                name=var.replace("_", " ").title(),
            )

        fig.update_layout(
            xaxis_title="Timestep",
            yaxis_title="Value",
            legend_title="Variables",
            height=350,
        )
        return fig

    # Display 2 x 2 grid
    grid = st.columns(2)

    actor_order = ["Students", "Professors", "Clubs", "Admins"]

    for idx, actor_group in enumerate(actor_order):
        with grid[idx % 2]:
            st.write(f"### {actor_group}")
            vars_list = groups[actor_group]

            if len(vars_list) == 0:
                st.info("No variables logged for this actor yet.")
                continue

            fig = create_group_plot(actor_group, vars_list)
            st.plotly_chart(fig, use_container_width=True)

    st.write("---")


def render_trends(world):
    st.header("📈 Simulation Trends")

    df, groups = world.get_grouped_history()

    # ---- 2x2 Grid Layout ----
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    panels = [
        (col1, "Students"),
        (col2, "Professors"),
        (col3, "Clubs"),
        (col4, "Admins"),
    ]

    for col, group_name in panels:
        with col:
            st.subheader(group_name)

            cols = groups[group_name]
            if not cols:
                st.info("No data yet.")
                continue

            # For each variable in the group, plot a line
            for var in cols:
                fig = px.line(df, x="timestep", y=var, title=var.replace("_", " ").title())
                fig.update_layout(height=250, showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)


    