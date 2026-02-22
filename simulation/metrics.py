# simulation/metrics.py

import traci
import csv
import os
from config.paths import Paths
from utils.logger import get_logger
from utils.metrics_store import metrics_store   # ← writes to shared store for UI

logger = get_logger(__name__)


class Metrics:
    def __init__(self):
        self.history         = []
        self._step_count     = 0
        self._arrived_total  = 0

    def update(self, phase_decisions: dict = None):
        self._step_count += 1
        vehicles = traci.vehicle.getIDList()

        step_wait  = 0.0
        step_queue = 0
        step_speed = 0.0
        step_co2   = 0.0
        step_fuel  = 0.0

        for v_id in vehicles:
            try:
                step_wait  += traci.vehicle.getWaitingTime(v_id)
                step_queue += 1 if traci.vehicle.isStopped(v_id) else 0
                step_speed += traci.vehicle.getSpeed(v_id)
                step_co2   += traci.vehicle.getCO2Emission(v_id)
                step_fuel  += traci.vehicle.getFuelConsumption(v_id)
            except Exception:
                pass

        n = max(len(vehicles), 1)
        arrived_this_step    = traci.simulation.getArrivedNumber()
        self._arrived_total += arrived_this_step

        record = {
            "step":               self._step_count,
            "vehicle_count":      len(vehicles),
            "avg_waiting_time":   round(step_wait  / n, 2),
            "total_queue":        step_queue,
            "avg_speed_ms":       round(step_speed / n, 2),
            "avg_speed_kmh":      round((step_speed / n) * 3.6, 1),
            "co2_mg":             round(step_co2, 1),
            "fuel_ml":            round(step_fuel, 1),
            "throughput":         arrived_this_step,
            "cumulative_arrived": self._arrived_total,
            "phases":             phase_decisions or {},
        }

        self.history.append(record)
        metrics_store.append(record)   # ← live push to UI

    def get_results(self) -> dict:
        if not self.history:
            return {}
        waits  = [r["avg_waiting_time"] for r in self.history]
        speeds = [r["avg_speed_kmh"]    for r in self.history]
        queues = [r["total_queue"]      for r in self.history]
        return {
            "total_steps":              self._step_count,
            "total_vehicles_arrived":   self._arrived_total,
            "avg_waiting_time_s":       round(sum(waits)  / len(waits),  2),
            "peak_queue":               max(queues),
            "avg_speed_kmh":            round(sum(speeds) / len(speeds), 1),
            "total_co2_mg":             sum(r["co2_mg"]   for r in self.history),
            "total_fuel_ml":            sum(r["fuel_ml"]  for r in self.history),
        }

    def export_csv(self, filepath: str = None) -> str:
        if not self.history:
            return ""
        filepath = filepath or os.path.join(Paths.LOGS_DIR, "metrics_history.csv")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        fieldnames = [k for k in self.history[0].keys() if k != "phases"]
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames + ["phases_str"])
            writer.writeheader()
            for row in self.history:
                flat = {k: v for k, v in row.items() if k != "phases"}
                flat["phases_str"] = str(row.get("phases", {}))
                writer.writerow(flat)
        logger.info("Metrics exported: %s", filepath)
        return filepath
