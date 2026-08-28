"""
Train the anomaly-detection model used by health_scoring.py
======================================================================
Run this ONCE (or whenever you get better data) to produce health_model.joblib.

Why IsolationForest: it's an unsupervised anomaly detector — you don't need
labeled "this track failed" data (which you don't have). You just show it a
pile of NORMAL sensor readings, and it learns what "normal" looks like. Any
reading that doesn't fit the pattern gets a low (anomalous) score. This is a
legitimate, genuinely-ML approach for a hackathon: no fake labels, no
overfitting to 3 examples.

Right now it trains on SYNTHETIC data (randomly generated healthy readings)
because there's no real sensor history yet. Swap `generate_synthetic_normal_data()`
for real historical readings the moment you have any — even a few hundred
logged readings from P1's simulator running for a while would improve this
a lot.

Usage:
    pip install scikit-learn joblib numpy
    python train_model.py
"""

import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

FEATURE_ORDER = ["vibration", "temperature", "axleLoad"]
MODEL_PATH = "health_model.joblib"


def generate_synthetic_normal_data(n_samples: int = 2000) -> np.ndarray:
    """
    Simulates what 'healthy' track sections look like. Ranges are loosely
    based on the MAX_VALUES in health_scoring.py, biased toward the low
    (healthy) end since most track time should be normal, not failing.
    """
    rng = np.random.default_rng(seed=42)
    vibration = rng.normal(loc=2.5, scale=1.0, size=n_samples).clip(0, 10)
    temperature = rng.normal(loc=35, scale=8, size=n_samples).clip(0, 100)
    axle_load = rng.normal(loc=16, scale=4, size=n_samples).clip(0, 40)
    return np.column_stack([vibration, temperature, axle_load])


def main():
    X = generate_synthetic_normal_data()

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,  # assume ~5% of readings look anomalous even in "normal" data
        random_state=42,
    )
    model.fit(X)

    joblib.dump({"model": model, "feature_order": FEATURE_ORDER}, MODEL_PATH)
    print(f"Trained on {len(X)} synthetic samples. Saved to {MODEL_PATH}")

    
    # Sanity check: a clearly bad reading should score much lower than a good one
    good = np.array([[2.0, 30, 15]])
    bad = np.array([[9.0, 90, 35]])
    print("Anomaly score (good reading, higher=more normal):", model.decision_function(good)[0])
    print("Anomaly score (bad reading, lower=more anomalous):", model.decision_function(bad)[0])


if __name__ == "__main__":
    main()
