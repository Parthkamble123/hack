# ui/components/charts.py

import streamlit as st
import pandas as pd
import numpy as np

class TrafficCharts:
    """
    Real-time line/bar charts for traffic simulation metrics.
    """

    def render(self, intersection):
        st.subheader(f"Traffic Metrics Charts: {intersection}")

        # Example dummy data
        data = pd.DataFrame({
            "Step": range(50),
            "Queue Length": np.random.randint(5, 20, 50),
            "Waiting Time": np.random.randint(5, 30, 50),
            "Average Speed": np.random.randint(25, 50, 50)
        })

        st.line_chart(data.set_index("Step")[["Queue Length", "Waiting Time"]])
        st.bar_chart(data.set_index("Step")[["Average Speed"]])