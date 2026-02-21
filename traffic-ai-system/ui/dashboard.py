# ui/dashboard.py

import streamlit as st
from components.control_panel import ControlPanel
from components.metrics_display import MetricsDisplay
from components.charts import TrafficCharts
from components.comparison_table import ComparisonTable

st.set_page_config(
    page_title="AI Traffic Signal Dashboard",
    layout="wide"
)

st.title("AI Traffic Signal Optimization System 🚦")

# --- Control Panel ---
control_panel = ControlPanel()
intersection, run_sim = control_panel.render()

# --- Live Metrics ---
metrics_display = MetricsDisplay()
metrics_display.render(intersection)

# --- Charts ---
charts = TrafficCharts()
charts.render(intersection)

# --- Comparison Table ---
comparison_table = ComparisonTable()
comparison_table.render()