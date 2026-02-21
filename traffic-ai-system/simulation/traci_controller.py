# simulation/traci_controller.py

import traci
from config.simulation_config import SimulationConfig
from config.paths import Paths


class TraCIController:
    """
    Handles SUMO start and stop using TraCI.
    """

    def __init__(self):
        self.sumo_binary = SimulationConfig.get_sumo_binary()
        self.config_file = Paths.SUMO_CONFIG_FILE
        self.running = False

    def start(self):
        traci.start([
            self.sumo_binary,
            "-c", self.config_file,
            *SimulationConfig.TRACI_OPTIONS
        ])
        self.running = True

    def step(self):
        if self.running:
            traci.simulationStep()

    def close(self):
        if self.running:
            traci.close()
            self.running = False