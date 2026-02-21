# simulation/metrics.py

import traci


class Metrics:
    """
    Collects simulation performance metrics.
    """

    def __init__(self):
        self.total_waiting_time = 0
        self.total_vehicles = 0

    def update(self):
        vehicles = traci.vehicle.getIDList()

        for v in vehicles:
            self.total_waiting_time += traci.vehicle.getWaitingTime(v)

        self.total_vehicles += len(vehicles)

    def get_results(self):
        avg_wait = 0
        if self.total_vehicles > 0:
            avg_wait = self.total_waiting_time / self.total_vehicles

        return {
            "total_vehicles": self.total_vehicles,
            "average_waiting_time": avg_wait
        }