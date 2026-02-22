# config/model_config.py

class ModelConfig:
    # Phase timing
    MIN_PHASE_DURATION    = 5
    MAX_PHASE_DURATION    = 60
    YELLOW_PHASE_DURATION = 3

    # Emergency override
    ENABLE_EMERGENCY_OVERRIDE = True
    EMERGENCY_VEHICLE_TYPES   = ["emergency", "ambulance", "firetruck", "police"]
    EMERGENCY_OVERRIDE_PHASE  = 0

    # Feature flags
    USE_QUEUE_LENGTH  = True
    USE_WAITING_TIME  = True
    USE_VEHICLE_COUNT = True
    USE_SPEED_FEATURE = True

    # Multi-intersection IDs (must match SUMO network)
    INTERSECTION_IDS = ["center"]
    PHASE_COUNT      = 4

    # AI confidence threshold
    CONFIDENCE_THRESHOLD = 0.55
