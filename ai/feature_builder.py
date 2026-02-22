# ai/feature_builder.py

import os
import numpy as np
import joblib
from simulation.state_extractor import StateExtractor
from config.model_config import ModelConfig
from config.paths import Paths
from utils.logger import get_logger

logger = get_logger(__name__)


class FeatureBuilder:
    def __init__(self, traffic_light_id: str):
        self.traffic_light_id = traffic_light_id
        self.extractor         = StateExtractor(traffic_light_id)
        self._scaler           = self._load_scaler()

    def _load_scaler(self):
        if os.path.exists(Paths.SCALER_FILE):
            try:
                scaler = joblib.load(Paths.SCALER_FILE)
                logger.info("Scaler loaded from %s", Paths.SCALER_FILE)
                return scaler
            except Exception as e:
                logger.warning("Could not load scaler: %s", e)
        else:
            logger.warning("Scaler not found — features will NOT be scaled")
        return None

    def build(self) -> np.ndarray:
        state    = self.extractor.get_state()
        per_lane = state.get("per_lane", {})

        if not per_lane:
            logger.warning("No lane data for %s", self.traffic_light_id)
            return np.zeros((1, 1))

        lanes = sorted(per_lane.keys())
        vehicle_counts, waiting_times, queue_lengths, mean_speeds = [], [], [], []

        for lane in lanes:
            info = per_lane[lane]
            if ModelConfig.USE_VEHICLE_COUNT: vehicle_counts.append(info["vehicle_count"])
            if ModelConfig.USE_WAITING_TIME:  waiting_times.append(info["waiting_time"])
            if ModelConfig.USE_QUEUE_LENGTH:  queue_lengths.append(info["queue_length"])
            if ModelConfig.USE_SPEED_FEATURE: mean_speeds.append(info["mean_speed"])

        raw      = vehicle_counts + waiting_times + queue_lengths + mean_speeds
        features = np.array(raw, dtype=float).reshape(1, -1)

        if self._scaler is not None:
            try:
                features = self._scaler.transform(features)
            except Exception as e:
                logger.warning("Scaler transform failed: %s", e)

        return features
