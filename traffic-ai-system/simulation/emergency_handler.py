# simulation/emergency_handler.py

import traci
from config.model_config import ModelConfig


class EmergencyHandler:
    """
    Detects emergency vehicles and forces override.
    """

    def __init__(self, traffic_light_id):
        self.traffic_light_id = traffic_light_id

    def check_emergency(self):
        if not ModelConfig.ENABLE_EMERGENCY_OVERRIDE:
            return False

        lanes = traci.trafficlight.getControlledLanes(self.traffic_light_id)

        for lane in lanes:
            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for vehicle_id in vehicles:
                vehicle_type = traci.vehicle.getTypeID(vehicle_id)

                if vehicle_type in ModelConfig.EMERGENCY_VEHICLE_TYPES:
                    traci.trafficlight.setPhase(
                        self.traffic_light_id,
                        ModelConfig.EMERGENCY_OVERRIDE_PHASE
                    )
                    return True

        return False