# training/evaluate.py

import joblib
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from config.paths import Paths

def evaluate_model():
    # Load model
    model = joblib.load(Paths.MODEL_FILE)
    
    # Load processed data
    X = np.load(Paths.X_TRAIN)
    y = np.load(Paths.Y_TRAIN)

    # Predict
    y_pred = model.predict(X)

    # Metrics
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    print(f"Evaluation results:\nMSE: {mse:.3f}\nR2 Score: {r2:.3f}")

if __name__ == "__main__":
    evaluate_model()