# src/components/simulation_controls.py
import streamlit as st
import time
import os


DATA_DIR = "/Users/keshava/Documents/micro-economy-simulator/data"  # same path you used


def render_simulation_controls(world, policy_updates):
    st.subheader("Simulation Controls")
    st.caption("Run, reset, save, or load simulations.")

    # Ensure flags exist
    for key in ("show_save_input", "show_load_input"):
        if key not in st.session_state:
            st.session_state[key] = False

    # Main control deck
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Run**")
            run_1 = st.button("Run 1 step", use_container_width=True)
            run_10 = st.button("Run 5 steps", use_container_width=True)

        with col2:
            st.markdown("**State**")
            reset = st.button("Reset simulation", use_container_width=True)

        with col3:
            st.markdown("**Persistence**")
            save = st.button("Save data", use_container_width=True)
            load = st.button("Load data", use_container_width=True)

    # --- Actions ---

    if run_1:
        world.step(policy_updates)
        st.session_state.world = world
        st.toast("Ran 1 step ✅")
        st.rerun()

    if run_10:
        for _ in range(5):
            world.step(policy_updates)
            st.session_state.world = world
        st.toast("Ran 5 steps ✅")
        st.rerun()

    if reset:
        from src.world import World  # same backend class
        st.session_state.world = World()
        st.success("Simulation reset successfully!")

    # Save popup
    if save:
        st.session_state.show_save_input = True

    if st.session_state.show_save_input:
        with st.container(border=True):
            st.markdown("#### Save current simulation")
            filename = st.text_input("Filename (without extension):", key="save_filename")

            c1, c2 = st.columns([1, 1])
            confirm = c1.button("Save")
            cancel = c2.button("Cancel")

            if confirm:
                if filename.strip() == "":
                    st.error("Filename cannot be empty!")
                else:
                    world.save_data(filename)  # ✅ same backend call
                    st.success(f"Data saved as `{filename}`")
                    st.session_state.show_save_input = False

            if cancel:
                st.session_state.show_save_input = False

    # Load popup
    if load:
        st.session_state.show_load_input = True

    if st.session_state.show_load_input:
        with st.container(border=True):
            st.markdown("#### Load saved simulation")

            if not os.path.isdir(DATA_DIR):
                st.info(f"No data folder found at `{DATA_DIR}`.")
                return

            files = [
                f for f in os.listdir(DATA_DIR)
                if os.path.isfile(os.path.join(DATA_DIR, f))
            ]

            if not files:
                st.info("No saved files found yet.")
            else:
                selected_file = st.selectbox("Choose a file to load", options=files)
                c1, c2 = st.columns([1, 1])
                confirm = c1.button("Load")
                cancel = c2.button("Cancel")

                if confirm:
                    world.load_data(selected_file)  # ✅ same backend call
                    st.session_state.world = world
                    st.success(f"Data loaded from `{selected_file}`")
                    st.session_state.show_load_input = False
                    st.rerun()

                if cancel:
                    st.session_state.show_load_input = False
