# ui/components/comparison_table.py

import streamlit as st
import pandas as pd
from config.model_config import ModelConfig


class ComparisonTable:
    def render(self, history: list):
        st.subheader("🔀 Intersection Comparison")

        if not history:
            st.info("Run simulation to populate.")
            return

        rows = []
        for tl_id in ModelConfig.INTERSECTION_IDS:
            waits  = [s.get("avg_waiting_time", 0) for s in history]
            queues = [s.get("total_queue", 0)       for s in history]
            speeds = [s.get("avg_speed_kmh", 0)     for s in history]
            phases = [s.get("phases", {}).get(tl_id) for s in history if tl_id in s.get("phases", {})]

            rows.append({
                "Intersection":   tl_id,
                "Avg Wait (s)":   round(sum(waits)  / max(len(waits),  1), 1),
                "Avg Queue":      round(sum(queues) / max(len(queues), 1), 1),
                "Avg Speed km/h": round(sum(speeds) / max(len(speeds), 1), 1),
                "Phase Changes":  len(set(p for p in phases if p is not None)),
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
