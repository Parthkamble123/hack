# ui/components/control_panel.py

import streamlit as st

class ControlPanel:
    """
    Control panel UI for simulation control.
    """

    def render(self):
        st.sidebar.header("Simulation Controls")
        run_simulation = st.sidebar.button("Run Simulation")
        pause_simulation = st.sidebar.button("Pause Simulation")

        intersection = st.sidebar.selectbox(
            "Select Intersection",
            ["center", "cross1", "cross2"]
        )

        return intersection, run_simulation