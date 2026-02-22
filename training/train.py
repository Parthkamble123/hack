# training/train.py

import os
import sys
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.preprocess import load_raw_data, preprocess, save_processed_data
from training.feature_engineering import build_features
from config.paths import Paths
from utils.logger import get_logger

logger = get_logger(__name__)


def train_model():
    logger.info("=== Training started ===")
    df = load_raw_data()
    df = preprocess(df)

    X, y, scaler = build_features(df)
    logger.info("Shape: %s | Classes: %s", X.shape, np.unique(y))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
        stratify=y if len(np.unique(y)) > 1 else None
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    logger.info("Classification Report:\n%s", classification_report(y_test, y_pred))

    cv = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    logger.info("CV Accuracy: %.3f ± %.3f", cv.mean(), cv.std())

    os.makedirs(Paths.MODELS_DIR, exist_ok=True)
    os.makedirs(Paths.PROCESSED_DATA_DIR, exist_ok=True)

    joblib.dump(model,  Paths.MODEL_FILE)
    joblib.dump(scaler, Paths.SCALER_FILE)
    save_processed_data(X_train, y_train, scaler)

    logger.info("Model saved: %s",  Paths.MODEL_FILE)
    logger.info("Scaler saved: %s", Paths.SCALER_FILE)
    logger.info("=== Training complete ===")
    return model, scaler


if __name__ == "__main__":
    train_model()
