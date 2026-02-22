# simulation/emergency_handler.py

import traci
from config.model_config import ModelConfig
from utils.logger import get_logger

logger = get_logger(__name__)


class EmergencyHandler:
    COOLDOWN_STEPS = 10

    def __init__(self, traffic_light_id: str):
        self.traffic_light_id = traffic_light_id
        self._cooldown         = 0

    def check_and_handle(self) -> bool:
        if not ModelConfig.ENABLE_EMERGENCY_OVERRIDE:
            return False

        emergency_lane = self._detect_emergency_lane()

        if emergency_lane is not None:
            target_phase = self._lane_to_green_phase(emergency_lane)
            try:
                traci.trafficlight.setPhase(self.traffic_light_id, target_phase)
                traci.trafficlight.setPhaseDuration(
                    self.traffic_light_id, float(self.COOLDOWN_STEPS)
                )
                logger.warning("EMERGENCY OVERRIDE: %s lane %s → phase %d",
                               self.traffic_light_id, emergency_lane, target_phase)
            except Exception as e:
                logger.error("Emergency override failed: %s", e)

            self._cooldown = self.COOLDOWN_STEPS
            return True

        if self._cooldown > 0:
            self._cooldown -= 1
            return True

        return False

    def _detect_emergency_lane(self):
        try:
            lanes = traci.trafficlight.getControlledLanes(self.traffic_light_id)
        except Exception:
            return None

        for lane in lanes:
            for v_id in traci.lane.getLastStepVehicleIDs(lane):
                try:
                    if traci.vehicle.getTypeID(v_id) in ModelConfig.EMERGENCY_VEHICLE_TYPES:
                        return lane
                except Exception:
                    continue
        return None

    def _lane_to_green_phase(self, lane_id: str) -> int:
        lane_lower = lane_id.lower()
        if any(d in lane_lower for d in ["n2c", "s2c"]):
            return 0
        if any(d in lane_lower for d in ["e2c", "w2c"]):
            return 2
        return ModelConfig.EMERGENCY_OVERRIDE_PHASE
