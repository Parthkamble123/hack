# config/system_config.py

import os

class SystemConfig:
    """
    Global system configuration.
    """

    ENVIRONMENT = os.getenv("APP_ENV", "development")
    DEBUG = ENVIRONMENT == "development"

    APP_NAME = "AI Traffic Signal System"
    VERSION = "1.0.0"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    ENABLE_PROFILING = False
    ENABLE_METRICS = True
    AUTO_START_SIMULATION = False