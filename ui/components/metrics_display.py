# ui/components/metrics_display.py

import streamlit as st


class MetricsDisplay:
    def render(self, intersection: str, history: list):
        """Live metrics from latest step."""
        if not history:
            st.info("No data yet — run the simulation.")
            return

        latest = history[-1]
        st.subheader(f"📊 Live — {intersection}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🚗 Vehicles",        latest.get("vehicle_count",    0))
        c2.metric("⏱ Avg Wait (s)",     latest.get("avg_waiting_time", 0))
        c3.metric("🛑 Queue",            latest.get("total_queue",      0))
        c4.metric("🏎 Speed (km/h)",    latest.get("avg_speed_kmh",    0))

    def render_summary(self, summary: dict):
        """Post-simulation KPI cards."""
        st.subheader("📋 Simulation Summary")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Arrived",   summary.get("total_vehicles_arrived", 0))
        c2.metric("Avg Wait (s)",    summary.get("avg_waiting_time_s",     0))
        c3.metric("Peak Queue",      summary.get("peak_queue",             0))
        c4.metric("Avg Speed km/h",  summary.get("avg_speed_kmh",          0))
        c5.metric("Total Steps",     summary.get("total_steps",            0))
        st.caption(
            f"CO₂: {summary.get('total_co2_mg', 0):,.0f} mg  |  "
            f"Fuel: {summary.get('total_fuel_ml', 0):,.0f} ml"
        )
