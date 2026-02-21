# config/simulation_config.py

import os

class SimulationConfig:
    """
    Simulation and SUMO runtime settings.
    """

    USE_GUI = os.getenv("SUMO_GUI", "True") == "True"
    STEP_LENGTH = 1  # seconds per simulation step
    MAX_STEPS = 10000
    AUTO_CLOSE_ON_END = True
    REAL_TIME_DELAY = 0.1  # For Streamlit UI sync

    TRACI_OPTIONS = ["--start", "--quit-on-end"]

    @staticmethod
    def get_sumo_binary():
        """
        Returns the SUMO binary path (GUI or headless)
        """
        sumo_home = os.environ.get("SUMO_HOME")
        if not sumo_home:
            raise EnvironmentError("SUMO_HOME environment variable is not set.")

        binary = "sumo-gui" if SimulationConfig.USE_GUI else "sumo"
        sumo_binary = os.path.join(sumo_home, "bin", binary)

        if not os.path.exists(sumo_binary):
            raise FileNotFoundError(f"SUMO binary not found at: {sumo_binary}")

        return sumo_binary