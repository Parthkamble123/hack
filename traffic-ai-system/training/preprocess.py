# training/preprocess.py

import pandas as pd
import numpy as np
from config.paths import Paths
from sklearn.preprocessing import StandardScaler
import os
import joblib

def load_raw_data():
    df = pd.read_csv(Paths.TRAFFIC_DATASET)
    return df

def preprocess(df):
    """
    Basic preprocessing: remove nulls, convert categorical features if needed
    """
    df = df.dropna()
    
    # Example: encode signal_id if categorical
    if 'signal_id' in df.columns:
        df = pd.get_dummies(df, columns=['signal_id'], drop_first=True)
        
    return df

def save_processed_data(X, y, scaler):
    os.makedirs(Paths.PROCESSED_DATA_DIR, exist_ok=True)
    np.save(Paths.X_TRAIN, X)
    np.save(Paths.Y_TRAIN, y)
    joblib.dump(scaler, Paths.SCALER)