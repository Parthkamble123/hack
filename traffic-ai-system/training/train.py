# training/train.py

import joblib
from sklearn.ensemble import RandomForestRegressor
from training.preprocess import load_raw_data, preprocess, save_processed_data
from training.feature_engineering import build_features
from config.paths import Paths
import os

def train_model():
    # Load & preprocess
    df = load_raw_data()
    df = preprocess(df)

    # Build features
    X, y, scaler = build_features(df)

    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X, y)

    # Save processed data
    save_processed_data(X, y, scaler)

    # Save trained model
    os.makedirs(Paths.MODELS_DIR, exist_ok=True)
    joblib.dump(model, Paths.MODEL_FILE)
    print(f"Model saved to {Paths.MODEL_FILE}")

if __name__ == "__main__":
    train_model()