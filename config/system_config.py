# config/system_config.py

import os
import logging

class SystemConfig:
    ENVIRONMENT    = os.getenv("APP_ENV", "development")
    DEBUG          = ENVIRONMENT == "development"
    APP_NAME       = "AI Traffic Signal System"
    VERSION        = "2.0.0"
    LOG_LEVEL      = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_METRICS = True
    AUTO_START_SIMULATION = False

    @staticmethod
    def setup_logging():
        os.makedirs("logs", exist_ok=True)
        level = getattr(logging, SystemConfig.LOG_LEVEL.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("logs/app.log", mode="a"),
            ]
        )

SystemConfig.setup_logging()
