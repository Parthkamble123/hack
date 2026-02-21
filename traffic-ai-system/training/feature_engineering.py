# training/feature_engineering.py

import numpy as np
from sklearn.preprocessing import StandardScaler

def build_features(df):
    """
    Create feature matrix X and target y
    Example: predicting next phase duration or congestion level
    """
    # Define features and target
    target_column = 'next_phase_duration'
    feature_columns = [col for col in df.columns if col != target_column]

    X = df[feature_columns].values
    y = df[target_column].values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler