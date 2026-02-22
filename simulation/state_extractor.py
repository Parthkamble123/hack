# simulation/state_extractor.py

import traci
from utils.logger import get_logger

logger = get_logger(__name__)


class StateExtractor:
    def __init__(self, traffic_light_id: str):
        self.traffic_light_id = traffic_light_id

    def get_state(self) -> dict:
        try:
            lanes = traci.trafficlight.getControlledLanes(self.traffic_light_id)
        except Exception as e:
            logger.error("Failed to get lanes for %s: %s", self.traffic_light_id, e)
            return self._empty_state()

        if not lanes:
            return self._empty_state()

        vehicle_count = 0
        waiting_time  = 0.0
        queue_length  = 0
        total_speed   = 0.0
        speed_samples = 0
        per_lane      = {}

        for lane in lanes:
            count  = traci.lane.getLastStepVehicleNumber(lane)
            wait   = traci.lane.getWaitingTime(lane)
            queue  = traci.lane.getLastStepHaltingNumber(lane)
            speed  = traci.lane.getLastStepMeanSpeed(lane)
            length = traci.lane.getLength(lane)
            density = (count / (length / 1000.0)) if length > 0 else 0.0

            vehicle_count += count
            waiting_time  += wait
            queue_length  += queue

            if count > 0:
                total_speed   += speed * count
                speed_samples += count

            per_lane[lane] = {
                "vehicle_count": count,
                "waiting_time":  wait,
                "queue_length":  queue,
                "mean_speed":    round(speed, 2),
                "density":       round(density, 2),
            }

        mean_speed     = (total_speed / speed_samples) if speed_samples > 0 else 0.0
        current_phase  = traci.trafficlight.getPhase(self.traffic_light_id)
        phase_duration = traci.trafficlight.getPhaseDuration(self.traffic_light_id)

        return {
            "traffic_light_id": self.traffic_light_id,
            "vehicle_count":    vehicle_count,
            "waiting_time":     round(waiting_time, 2),
            "queue_length":     queue_length,
            "mean_speed":       round(mean_speed, 2),
            "current_phase":    current_phase,
            "phase_duration":   phase_duration,
            "per_lane":         per_lane,
        }

    @staticmethod
    def _empty_state() -> dict:
        return {
            "traffic_light_id": "",
            "vehicle_count": 0, "waiting_time": 0.0,
            "queue_length": 0,  "mean_speed": 0.0,
            "current_phase": 0, "phase_duration": 30.0,
            "per_lane": {},
        }
