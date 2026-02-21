# simulation/simulation_manager.py

import time
from config.simulation_config import SimulationConfig
from config.paths import Paths
from simulation.traci_controller import TraCIController
from simulation.coordination_manager import CoordinationManager
from simulation.metrics import Metrics


class SimulationManager:
    """
    Full simulation lifecycle manager.
    """

    def __init__(self):
        Paths.validate()

        self.traci_controller = TraCIController()
        self.coordination_manager = CoordinationManager()
        self.metrics = Metrics()

    def run(self):
        self.traci_controller.start()

        try:
            for step in range(SimulationConfig.MAX_STEPS):
                self.traci_controller.step()

                # Multi-intersection AI decision
                self.coordination_manager.step()

                # Metrics update
                self.metrics.update()

                # Optional real-time delay (for UI sync)
                if SimulationConfig.REAL_TIME_DELAY > 0:
                    time.sleep(SimulationConfig.REAL_TIME_DELAY)

        finally:
            self.traci_controller.close()

        return self.metrics.get_results()