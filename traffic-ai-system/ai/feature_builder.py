# ai/feature_builder.py

import traci
import numpy as np


class FeatureBuilder:
    """
    Extracts traffic features from SUMO and
    builds ML-ready feature vector.
    """

    def __init__(self, lane_ids=None):
        """
        lane_ids: Optional predefined lane order.
        If None → auto-detect from SUMO.
        """
        self.lane_ids = lane_ids

    def _get_lane_ids(self):
        if self.lane_ids is not None:
            return self.lane_ids

        return sorted(traci.lane.getIDList())

    def build(self):
        """
        Returns:
            np.ndarray shape (1, N)
        """

        lane_ids = self._get_lane_ids()

        vehicle_counts = []
        waiting_times = []

        for lane in lane_ids:
            vehicle_counts.append(
                traci.lane.getLastStepVehicleNumber(lane)
            )

            waiting_times.append(
                traci.lane.getWaitingTime(lane)
            )

        # Feature vector format:
        # [count_lane1, count_lane2, ..., wait_lane1, wait_lane2, ...]
        features = np.array(
            vehicle_counts + waiting_times,
            dtype=float
        ).reshape(1, -1)

        return features