# ui/components/control_panel.py

import streamlit as st
from config.model_config import ModelConfig
from config.simulation_config import SimulationConfig


class ControlPanel:
    def render(self):
        st.header("🚦 Controls")

        intersection = st.selectbox(
            "Select Intersection",
            options=ModelConfig.INTERSECTION_IDS + ["cross1", "cross2"],
            index=0,
        )

        with st.expander("⚙️ Config"):
            st.write(f"**Max Steps:** {SimulationConfig.MAX_STEPS}")
            st.write(f"**Step Length:** {SimulationConfig.STEP_LENGTH}s")
            st.write(f"**GUI Mode:** {SimulationConfig.USE_GUI}")
            st.write(f"**Min Phase:** {ModelConfig.MIN_PHASE_DURATION} steps")
            st.write(f"**Max Phase:** {ModelConfig.MAX_PHASE_DURATION} steps")
            st.write(f"**Emergency Override:** {ModelConfig.ENABLE_EMERGENCY_OVERRIDE}")

        st.divider()
        run_clicked  = st.button("▶️ Run Simulation",  type="primary",   use_container_width=True)
        stop_clicked = st.button("⏹️ Stop",            type="secondary", use_container_width=True)

        return intersection, run_clicked, stop_clicked
