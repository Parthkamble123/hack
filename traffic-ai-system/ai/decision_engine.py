# ai/decision_engine.py

import traci


class DecisionEngine:
    """
    Connects:
    FeatureBuilder → Predictor → SUMO traffic light control
    Supports:
        - Min phase duration
        - Emergency vehicle override
    """

    def __init__(
        self,
        model_loader,
        feature_builder,
        predictor,
        traffic_light_id="center",
        min_phase_duration=5
    ):
        self.model_loader = model_loader
        self.feature_builder = feature_builder
        self.predictor = predictor
        self.traffic_light_id = traffic_light_id
        self.min_phase_duration = min_phase_duration

        self._last_phase = None
        self._phase_timer = 0

    def _can_switch(self):
        return self._phase_timer >= self.min_phase_duration

    def _check_emergency(self):
        """
        Returns True if any emergency vehicle is detected
        on any lane controlled by this traffic light.
        """
        controlled_lanes = traci.trafficlight.getControlledLanes(
            self.traffic_light_id
        )

        for lane in controlled_lanes:
            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for v_id in vehicles:
                # SUMO allows vehicle type checking
                if traci.vehicle.getTypeID(v_id) in ["ambulance", "firetruck", "police"]:
                    return True
        return False

    def step(self):
        """
        Called every simulation step.
        """

        # Emergency override
        if self._check_emergency():
            # Switch to green phase for emergency lanes
            # Simplified: set to predefined "emergency" phase (0)
            traci.trafficlight.setPhase(self.traffic_light_id, 0)
            self._phase_timer = 0
            self._last_phase = 0
            return 0

        # Build features
        features = self.feature_builder.build()

        # Predict phase
        predicted_phase = self.predictor.predict(features)

        current_phase = traci.trafficlight.getPhase(
            self.traffic_light_id
        )

        # Prevent rapid oscillation
        if predicted_phase != current_phase:
            if self._can_switch():
                traci.trafficlight.setPhase(
                    self.traffic_light_id,
                    predicted_phase
                )
                self._phase_timer = 0
                self._last_phase = predicted_phase
        else:
            self._phase_timer += 1

        return predicted_phase