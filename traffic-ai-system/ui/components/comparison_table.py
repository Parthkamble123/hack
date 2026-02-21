# ui/components/comparison_table.py

import streamlit as st
import pandas as pd
import numpy as np

class ComparisonTable:
    """
    Display comparison table of intersections.
    """

    def render(self):
        st.subheader("Intersection Comparison Table")

        # Example dummy data
        data = pd.DataFrame({
            "Intersection": ["center", "cross1", "cross2"],
            "Avg Queue": [15, 10, 12],
            "Avg Waiting Time": [12, 8, 10],
            "Avg Speed (km/h)": [35, 40, 38]
        })

        st.table(data)