# ai/decision_engine.py

import traci
from config.model_config import ModelConfig
from simulation.emergency_handler import EmergencyHandler
from utils.logger import get_logger

logger = get_logger(__name__)


class DecisionEngine:
    def __init__(self, feature_builder, predictor, traffic_light_id: str = "center"):
        self.feature_builder   = feature_builder
        self.predictor         = predictor
        self.traffic_light_id  = traffic_light_id
        self.emergency_handler = EmergencyHandler(traffic_light_id)
        self._phase_timer      = 0
        self._in_yellow        = False

    def step(self) -> int:
        # Emergency takes priority
        if self.emergency_handler.check_and_handle():
            self._phase_timer = 0
            return traci.trafficlight.getPhase(self.traffic_light_id)

        # Don't interrupt yellow
        if self._in_yellow:
            self._phase_timer += 1
            if self._phase_timer >= ModelConfig.YELLOW_PHASE_DURATION:
                self._in_yellow   = False
                self._phase_timer = 0
            return traci.trafficlight.getPhase(self.traffic_light_id)

        current_phase = traci.trafficlight.getPhase(self.traffic_light_id)
        self._phase_timer += 1

        can_switch  = self._phase_timer >= ModelConfig.MIN_PHASE_DURATION
        must_switch = self._phase_timer >= ModelConfig.MAX_PHASE_DURATION

        if not can_switch:
            return current_phase

        features        = self.feature_builder.build()
        predicted_phase = self.predictor.predict(features, current_phase)

        if predicted_phase != current_phase or must_switch:
            self._insert_yellow_and_switch(current_phase, predicted_phase)

        return traci.trafficlight.getPhase(self.traffic_light_id)

    def _insert_yellow_and_switch(self, from_phase: int, to_phase: int):
        yellow_phase = from_phase + 1
        try:
            phase_count = len(
                traci.trafficlight.getAllProgramLogics(self.traffic_light_id)[0].phases
            )
        except Exception:
            phase_count = ModelConfig.PHASE_COUNT

        if yellow_phase < phase_count:
            traci.trafficlight.setPhase(self.traffic_light_id, yellow_phase)
            traci.trafficlight.setPhaseDuration(
                self.traffic_light_id, float(ModelConfig.YELLOW_PHASE_DURATION)
            )
            self._in_yellow   = True
            self._phase_timer = 0
            logger.debug("[%s] Yellow %d → switching to %d", self.traffic_light_id, yellow_phase, to_phase)
        else:
            traci.trafficlight.setPhase(self.traffic_light_id, to_phase)
            self._phase_timer = 0
            logger.info("[%s] Phase switch %d → %d", self.traffic_light_id, from_phase, to_phase)
