# ai/model_loader.py

import os
import joblib


class ModelLoader:
    """
    Loads and validates a trained ML model.
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self._model = None

    def load(self):
        """
        Loads model from disk.
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found at: {self.model_path}"
            )

        try:
            self._model = joblib.load(self.model_path)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model: {e}"
            )

        return self._model

    def get_model(self):
        """
        Returns loaded model.
        """
        if self._model is None:
            raise ValueError("Model not loaded. Call load() first.")

        return self._model