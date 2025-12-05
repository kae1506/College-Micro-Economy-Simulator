import streamlit as st
import time
import os

def render_simulation_controls(world, policy_updates):
    st.subheader("Simulation Controls")

    for key in ("show_save_input", "show_load_input"):
        if key not in st.session_state:
            st.session_state[key] = False
    
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("Run 1 Step"):
        print("ENTER ENTER ENTER")
        world.step(policy_updates)
        st.session_state.world = world
        st.rerun()              

    if col2.button("Run 10 Steps"):
        for _ in range(10):
            world.step(policy_updates)
            time.sleep(0.05)
            st.session_state.world = world

            st.rerun()

    if col3.button("Reset"):
        from world import World
        st.session_state.world = World()
        st.success("Simulation reset successfully!")

    # create a flag in session state if not present
    if "show_save_input" not in st.session_state:
        st.session_state.show_save_input = False

    if col4.button("Save Data"):
        st.session_state.show_save_input = True

    # if Save clicked → show input + submit button
    if st.session_state.show_save_input:
        st.write("### Enter filename to save data")

        filename = st.text_input("Filename:", key="save_filename")

        if st.button("Submit Save"):
            if filename.strip() == "":
                st.error("Filename cannot be empty!")
            else:
                world.save_data(filename)
                st.success(f"Data saved as `{filename}`")
                # reset the popup
                st.session_state.show_save_input = False

    if col5.button("Load Data"):
        st.session_state.show_load_input = True

    if st.session_state.show_load_input:
        with st.container(border=True):
            # st.write("### 📂 Enter filename to load data")

            # load_name = st.text_input("Load from:", key="load_filename")

            # if st.button("Confirm Load"):
            #     if load_name.strip() == "":
            #         st.error("Filename cannot be empty!")
            #     else:
            #         try:
            #             world.load_data(load_name)
            #             st.session_state.world = world
            #             st.success(f"Data loaded from `{load_name}`")
            #             st.session_state.show_load_input = False
            #             st.rerun()
            #         except FileNotFoundError:
            #             st.error("File not found — double check the name!")
                        


            DATA_DIR = "/Users/keshava/Documents/micro-economy-simulator/data"  # change this to your folder path

            # Get only files (not folders)
            files = [
                f for f in os.listdir(DATA_DIR)
                if os.path.isfile(os.path.join(DATA_DIR, f))
            ]

            selected_file = st.selectbox(
                "Load Dataset",
                options=["None"] + files
            )

            if selected_file != "None":
                world.load_data(selected_file)
                st.session_state.world = world
                st.success(f"Data loaded from `{load_name}`")
                st.session_state.show_load_input = False
                st.rerun()
