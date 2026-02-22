# training/preprocess.py

import pandas as pd
import numpy as np
import os
import joblib
from config.paths import Paths
from utils.logger import get_logger

logger = get_logger(__name__)


def load_raw_data() -> pd.DataFrame:
    df = pd.read_csv(Paths.TRAFFIC_DATASET)
    logger.info("Loaded %d rows × %d cols from %s", len(df), len(df.columns), Paths.TRAFFIC_DATASET)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    initial = df.shape
    df = df.drop_duplicates()

    nulls = df.isnull().sum()
    if nulls.any():
        logger.warning("Nulls found:\n%s", nulls[nulls > 0])
    df = df.dropna()

    for col in df.select_dtypes(include=[object]).columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass

    for col in df.columns:
        if any(k in col.lower() for k in ["count", "time", "queue", "speed"]):
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].clip(lower=0)

    if "signal_id" in df.columns:
        df["signal_id"] = pd.Categorical(df["signal_id"]).codes

    logger.info("Preprocessed: %s → %s", initial, df.shape)
    return df


def save_processed_data(X, y, scaler):
    os.makedirs(Paths.PROCESSED_DATA_DIR, exist_ok=True)
    np.save(Paths.X_TRAIN, X)
    np.save(Paths.Y_TRAIN, y)
    joblib.dump(scaler, Paths.SCALER)
    logger.info("Saved processed data to %s", Paths.PROCESSED_DATA_DIR)
