# config/paths.py

import os

class Paths:
    """
    Centralized path management for the project.
    """

    BASE_DIR = os.path.abspath(os.getcwd())

    # Data directories
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, "external")

    # Model directory
    MODELS_DIR = os.path.join(BASE_DIR, "models")

    # Simulation directories
    SIMULATION_DIR = os.path.join(BASE_DIR, "simulation")
    SUMO_CONFIG_DIR = os.path.join(SIMULATION_DIR, "sumo_config")

    # Specific files
    TRAFFIC_DATASET = os.path.join(RAW_DATA_DIR, "traffic_dataset.csv")
    X_TRAIN = os.path.join(PROCESSED_DATA_DIR, "X_train.npy")
    Y_TRAIN = os.path.join(PROCESSED_DATA_DIR, "y_train.npy")
    SCALER = os.path.join(PROCESSED_DATA_DIR, "scaler.pkl")
    MODEL_FILE = os.path.join(MODELS_DIR, "traffic_model.pkl")
    SUMO_CONFIG_FILE = os.path.join(SUMO_CONFIG_DIR, "simulation.sumocfg")
    NETWORK_FILE = os.path.join(SUMO_CONFIG_DIR, "network.net.xml")
    ROUTES_FILE = os.path.join(SUMO_CONFIG_DIR, "routes.rou.xml")

    @staticmethod
    def validate():
        """
        Ensure critical files exist before running the system.
        """
        required_files = [
            Paths.SUMO_CONFIG_FILE,
            Paths.MODEL_FILE,
            Paths.TRAFFIC_DATASET
        ]
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required file not found: {file}")