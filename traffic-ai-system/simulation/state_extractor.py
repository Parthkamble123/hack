# simulation/state_extractor.py

import traci


class StateExtractor:
    """
    Extracts real-time traffic state from SUMO.
    """

    def __init__(self, traffic_light_id):
        self.traffic_light_id = traffic_light_id

    def get_state(self):
        lanes = traci.trafficlight.getControlledLanes(self.traffic_light_id)

        vehicle_count = 0
        waiting_time = 0
        queue_length = 0

        for lane in lanes:
            vehicle_count += traci.lane.getLastStepVehicleNumber(lane)
            waiting_time += traci.lane.getWaitingTime(lane)
            queue_length += traci.lane.getLastStepHaltingNumber(lane)

        return {
            "vehicle_count": vehicle_count,
            "waiting_time": waiting_time,
            "queue_length": queue_length
        }