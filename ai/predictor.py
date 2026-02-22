# ai/predictor.py

import numpy as np
from config.model_config import ModelConfig
from utils.logger import get_logger

logger = get_logger(__name__)


class Predictor:
    def __init__(self, model):
        self.model        = model
        self._has_proba   = hasattr(model, "predict_proba")
        self._phase_count = ModelConfig.PHASE_COUNT

    def predict(self, features: np.ndarray, current_phase: int = 0) -> int:
        if features is None or features.size == 0:
            return current_phase

        try:
            if self._has_proba:
                proba      = self.model.predict_proba(features)[0]
                best_idx   = int(np.argmax(proba))
                confidence = float(proba[best_idx])

                if confidence < ModelConfig.CONFIDENCE_THRESHOLD:
                    logger.debug("Low confidence %.2f — keeping phase %d", confidence, current_phase)
                    return current_phase

                predicted = best_idx
            else:
                predicted = int(round(float(self.model.predict(features)[0])))

        except Exception as e:
            logger.error("Prediction failed: %s", e)
            return current_phase

        return max(0, min(predicted, self._phase_count - 1))
