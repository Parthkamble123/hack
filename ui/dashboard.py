# ui/dashboard.py
# Run with: streamlit run ui/dashboard.py  (from project root)

import sys
import os
import threading
import time
import streamlit as st

# Make sure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.system_config import SystemConfig
from ui.components.control_panel import ControlPanel
from ui.components.metrics_display import MetricsDisplay
from ui.components.charts import TrafficCharts
from ui.components.comparison_table import ComparisonTable
from utils.metrics_store import metrics_store

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Traffic Signal System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Title ──────────────────────────────────────────────────────────────────────
st.title("🚦 AI Traffic Signal Control System")
st.caption(f"v{SystemConfig.VERSION}  |  SUMO + ML-powered adaptive signal control")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    panel = ControlPanel()
    selected_intersection, run_clicked, stop_clicked = panel.render()

# ── Background simulation thread ───────────────────────────────────────────────
def _run_simulation():
    from simulation.simulation_manager import SimulationManager
    try:
        mgr = SimulationManager()
        mgr.run()
    except Exception as e:
        metrics_store.set_error(str(e))
        metrics_store.set_running(False)

if run_clicked and not metrics_store.is_running():
    metrics_store.reset()
    t = threading.Thread(target=_run_simulation, daemon=True)
    t.start()

# ── Status banner ──────────────────────────────────────────────────────────────
if metrics_store.is_running():
    st.info("⏳ Simulation running...")
elif metrics_store.get_error():
    st.error(f"❌ Error: {metrics_store.get_error()}")
elif metrics_store.get_summary():
    st.success("✅ Simulation complete!")

# ── Main layout ────────────────────────────────────────────────────────────────
history = metrics_store.get_history()
summary = metrics_store.get_summary()

metrics_ui  = MetricsDisplay()
charts_ui   = TrafficCharts()
comparison  = ComparisonTable()

if summary:
    metrics_ui.render_summary(summary)
    st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    metrics_ui.render(selected_intersection, history)
    charts_ui.render(selected_intersection, history)

with col_right:
    comparison.render(history)

# ── Auto-refresh while running ─────────────────────────────────────────────────
if metrics_store.is_running():
    time.sleep(1)
    st.rerun()
