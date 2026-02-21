# ui/components/metrics_display.py

import streamlit as st

class MetricsDisplay:
    """
    Display live traffic metrics: waiting times, queue lengths, average speed.
    """

    def render(self, intersection):
        st.subheader(f"Metrics for Intersection: {intersection}")
        col1, col2, col3 = st.columns(3)

        # Placeholder metrics
        col1.metric("Queue Length", "15 vehicles")
        col2.metric("Average Waiting Time", "12 sec")
        col3.metric("Average Speed", "35 km/h")