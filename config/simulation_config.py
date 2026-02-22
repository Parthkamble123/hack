# config/simulation_config.py

import os
import shutil


class SimulationConfig:
    USE_GUI = True
    STEP_LENGTH     = float(os.getenv("STEP_LENGTH", "1.0"))
    MAX_STEPS       = int(os.getenv("MAX_STEPS", "3600"))
    REAL_TIME_DELAY = 0.0
    SEED            = 42
    TRACI_PORT      = int(os.getenv("TRACI_PORT", "8813"))

    TRACI_OPTIONS = [
        f"--step-length={STEP_LENGTH}",
        f"--seed={SEED}",
        f"--remote-port={TRACI_PORT}",
        "--no-warnings",
        "--log", "logs/sumo.log",
    ]

    @staticmethod
    def get_sumo_binary() -> str:
        sumo_home = os.environ.get("SUMO_HOME")
        binary_name = "sumo-gui" if SimulationConfig.USE_GUI else "sumo"

        if sumo_home:
            candidate = os.path.join(sumo_home, "bin", binary_name)
            if os.path.exists(candidate):
                return candidate

        on_path = shutil.which(binary_name)
        if on_path:
            return on_path

        raise FileNotFoundError(
            f"SUMO binary '{binary_name}' not found. "
            "Set SUMO_HOME or add SUMO to your PATH."
        )