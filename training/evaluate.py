# training/evaluate.py

import sys
import os
import joblib
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.paths import Paths
from utils.logger import get_logger

logger = get_logger(__name__)


def evaluate_model():
    model = joblib.load(Paths.MODEL_FILE)
    X     = np.load(Paths.X_TRAIN)
    y     = np.load(Paths.Y_TRAIN)

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
        stratify=y if len(np.unique(y)) > 1 else None
    )

    y_pred = model.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)

    logger.info("Test Accuracy: %.4f", acc)
    logger.info("Report:\n%s", classification_report(y_test, y_pred))
    logger.info("Confusion Matrix:\n%s", confusion_matrix(y_test, y_pred))

    return {"accuracy": acc}


if __name__ == "__main__":
    evaluate_model()
