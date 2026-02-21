# config/model_config.py

class ModelConfig:
    """
    Configuration for AI model and decision engine.
    """

    # Minimum time before switching phase
    MIN_PHASE_DURATION = 5

    # Emergency override settings
    ENABLE_EMERGENCY_OVERRIDE = True
    EMERGENCY_VEHICLE_TYPES = ["ambulance", "firetruck", "police"]
    EMERGENCY_OVERRIDE_PHASE = 0

    # Features used by AI
    USE_QUEUE_LENGTH = True
    USE_WAITING_TIME = True
    USE_VEHICLE_COUNT = True

    # Multi-intersection support
    INTERSECTION_IDS = ["center"]  # add more as needed

    # Decision confidence threshold
    CONFIDENCE_THRESHOLD = 0.6