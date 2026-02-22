# generate_data.py
# Run this ONCE if you don't have a real traffic_dataset.csv
# python generate_data.py

import os
import numpy as np
import pandas as pd

np.random.seed(42)
N = 10000

# Simulate 2-lane intersection state
data = {
    "vehicle_count_n2c_0": np.random.randint(0, 20, N),
    "vehicle_count_n2c_1": np.random.randint(0, 20, N),
    "vehicle_count_s2c_0": np.random.randint(0, 20, N),
    "vehicle_count_s2c_1": np.random.randint(0, 20, N),
    "vehicle_count_e2c_0": np.random.randint(0, 20, N),
    "vehicle_count_e2c_1": np.random.randint(0, 20, N),
    "vehicle_count_w2c_0": np.random.randint(0, 20, N),
    "vehicle_count_w2c_1": np.random.randint(0, 20, N),

    "waiting_time_n2c_0":  np.random.uniform(0, 90, N),
    "waiting_time_n2c_1":  np.random.uniform(0, 90, N),
    "waiting_time_s2c_0":  np.random.uniform(0, 90, N),
    "waiting_time_s2c_1":  np.random.uniform(0, 90, N),
    "waiting_time_e2c_0":  np.random.uniform(0, 90, N),
    "waiting_time_e2c_1":  np.random.uniform(0, 90, N),
    "waiting_time_w2c_0":  np.random.uniform(0, 90, N),
    "waiting_time_w2c_1":  np.random.uniform(0, 90, N),

    "queue_length_n2c_0":  np.random.randint(0, 15, N),
    "queue_length_n2c_1":  np.random.randint(0, 15, N),
    "queue_length_s2c_0":  np.random.randint(0, 15, N),
    "queue_length_s2c_1":  np.random.randint(0, 15, N),
    "queue_length_e2c_0":  np.random.randint(0, 15, N),
    "queue_length_e2c_1":  np.random.randint(0, 15, N),
    "queue_length_w2c_0":  np.random.randint(0, 15, N),
    "queue_length_w2c_1":  np.random.randint(0, 15, N),

    "mean_speed_n2c_0":    np.random.uniform(0, 14, N),
    "mean_speed_n2c_1":    np.random.uniform(0, 14, N),
    "mean_speed_s2c_0":    np.random.uniform(0, 14, N),
    "mean_speed_s2c_1":    np.random.uniform(0, 14, N),
    "mean_speed_e2c_0":    np.random.uniform(0, 14, N),
    "mean_speed_e2c_1":    np.random.uniform(0, 14, N),
    "mean_speed_w2c_0":    np.random.uniform(0, 14, N),
    "mean_speed_w2c_1":    np.random.uniform(0, 14, N),
}

df = pd.DataFrame(data)

# Smart label: give green to whichever axis has more waiting vehicles
ns_pressure = (df["vehicle_count_n2c_0"] + df["vehicle_count_n2c_1"] +
               df["vehicle_count_s2c_0"] + df["vehicle_count_s2c_1"])
ew_pressure = (df["vehicle_count_e2c_0"] + df["vehicle_count_e2c_1"] +
               df["vehicle_count_w2c_0"] + df["vehicle_count_w2c_1"])

df["optimal_phase"] = np.where(ns_pressure >= ew_pressure, 0, 2)

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/traffic_dataset.csv", index=False)
print(f"✅ Dataset created: data/raw/traffic_dataset.csv ({len(df)} rows)")
print(f"   Phase 0 (NS green): {(df['optimal_phase']==0).sum()}")
print(f"   Phase 2 (EW green): {(df['optimal_phase']==2).sum()}")
