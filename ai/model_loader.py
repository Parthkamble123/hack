# ai/model_loader.py

import os
import joblib
from utils.logger import get_logger

logger = get_logger(__name__)


class ModelLoader:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self._model     = None

    def load(self):
        if self._model is not None:
            return self._model

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model not found: {self.model_path}\n"
                "Run: python -m training.train"
            )

        try:
            self._model = joblib.load(self.model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}") from e

        if not hasattr(self._model, "predict"):
            raise TypeError(f"Object has no predict(): {type(self._model)}")

        logger.info("Model loaded: %s", type(self._model).__name__)
        return self._model

    def reload(self):
        self._model = None
        return self.load()

    def get_model(self):
        if self._model is None:
            raise ValueError("Model not loaded. Call load() first.")
        return self._model
