# ui/components/charts.py

import streamlit as st
import pandas as pd


class TrafficCharts:
    def render(self, intersection: str, history: list):
        st.subheader(f"📈 Metrics Over Time — {intersection}")

        if not history:
            st.info("Run the simulation to see live charts.")
            return

        df = pd.DataFrame(history)

        cols = [c for c in ["avg_waiting_time", "total_queue", "avg_speed_kmh"] if c in df.columns]
        if cols:
            st.line_chart(df.set_index("step")[cols], height=250)

        if "throughput" in df.columns:
            st.subheader("🚗 Throughput (vehicles/step)")
            st.bar_chart(df.set_index("step")["throughput"], height=150)

        if "co2_mg" in df.columns:
            st.subheader("🌿 CO₂ (mg/step)")
            st.area_chart(df.set_index("step")["co2_mg"], height=150)
