# training/feature_engineering.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from utils.logger import get_logger

logger = get_logger(__name__)

TARGET_COLUMN = "optimal_phase"


def build_features(df: pd.DataFrame):
    if TARGET_COLUMN not in df.columns:
        phase_cols = [c for c in df.columns if "phase" in c.lower()]
        target = phase_cols[0] if phase_cols else df.columns[-1]
        logger.warning("'%s' not found — using '%s' as target", TARGET_COLUMN, target)
    else:
        target = TARGET_COLUMN

    feature_cols = [c for c in df.columns if c != target]

    # Match FeatureBuilder order: counts, waits, queues, speeds
    ordered = []
    for pattern in ["vehicle_count", "count", "waiting_time", "wait", "queue", "speed"]:
        matching = [c for c in feature_cols if pattern in c.lower() and c not in ordered]
        ordered.extend(matching)
    ordered.extend([c for c in feature_cols if c not in ordered])

    logger.info("Features (%d): %s | Target: %s", len(ordered), ordered, target)

    X = df[ordered].values.astype(float)
    y = df[target].values.astype(int)

    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler
