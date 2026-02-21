# ai/predictor.py


class Predictor:
    """
    Wraps ML model prediction logic.
    """

    def __init__(self, model):
        self.model = model

    def predict(self, features):
        """
        Predicts optimal traffic signal phase.

        Returns:
            int → phase index
        """

        if features is None:
            raise ValueError("Features cannot be None.")

        try:
            prediction = self.model.predict(features)
        except Exception as e:
            raise RuntimeError(
                f"Model prediction failed: {e}"
            )

        # Ensure integer output
        return int(prediction[0])