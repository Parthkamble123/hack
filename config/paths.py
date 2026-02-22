# config/paths.py

import os

class Paths:
    # Root = parent of config/
    BASE_DIR           = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Data
    DATA_DIR           = os.path.join(BASE_DIR, "data")
    RAW_DATA_DIR       = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    EXTERNAL_DATA_DIR  = os.path.join(DATA_DIR, "external")

    # Logs
    LOGS_DIR           = os.path.join(BASE_DIR, "logs")

    # Models
    MODELS_DIR         = os.path.join(BASE_DIR, "models")
    MODEL_FILE         = os.path.join(MODELS_DIR, "traffic_model.pkl")
    SCALER_FILE        = os.path.join(PROCESSED_DATA_DIR, "scaler.pkl")

    # Training data
    TRAFFIC_DATASET    = os.path.join(RAW_DATA_DIR, "traffic_dataset.csv")
    X_TRAIN            = os.path.join(PROCESSED_DATA_DIR, "X_train.npy")
    Y_TRAIN            = os.path.join(PROCESSED_DATA_DIR, "y_train.npy")
    SCALER             = os.path.join(PROCESSED_DATA_DIR, "scaler.pkl")

    # SUMO
    SIMULATION_DIR     = os.path.join(BASE_DIR, "simulation")
    SUMO_CONFIG_DIR    = os.path.join(SIMULATION_DIR, "sumo_config")
    SUMO_CONFIG_FILE   = os.path.join(SUMO_CONFIG_DIR, "simulation.sumocfg")
    NETWORK_FILE       = os.path.join(SUMO_CONFIG_DIR, "network.net.xml")
    ROUTES_FILE        = os.path.join(SUMO_CONFIG_DIR, "routes.rou.xml")
    DETECTOR_OUTPUT    = os.path.join(SUMO_CONFIG_DIR, "detector_output.xml")

    @staticmethod
    def ensure_dirs():
        for d in [
            Paths.RAW_DATA_DIR,
            Paths.PROCESSED_DATA_DIR,
            Paths.EXTERNAL_DATA_DIR,
            Paths.MODELS_DIR,
            Paths.LOGS_DIR,
        ]:
            os.makedirs(d, exist_ok=True)

    @staticmethod
    def validate():
        Paths.ensure_dirs()
        if not os.path.exists(Paths.SUMO_CONFIG_FILE):
            raise FileNotFoundError(f"SUMO config not found: {Paths.SUMO_CONFIG_FILE}")
        for label, path in [("Model", Paths.MODEL_FILE), ("Dataset", Paths.TRAFFIC_DATASET)]:
            if not os.path.exists(path):
                print(f"[Paths] WARNING: {label} not found at {path} — run training first.")
