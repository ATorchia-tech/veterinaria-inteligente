from __future__ import annotations
from datetime import date, timedelta
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

from app.external.weather_client import get_weather_features

MODELS_DIR = Path(__file__).resolve().parent / "models"
MODEL_PATH = MODELS_DIR / "noshow.joblib"


def _vectorize(
    day: date, hour: int, temp_avg: float, precip_prob: float, is_weekend: int
) -> np.ndarray:
    return np.array([is_weekend, hour, temp_avg, precip_prob], dtype=float)


def _synth_data(n_days: int = 200) -> tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    start = date.today() - timedelta(days=n_days)
    for i in range(n_days):
        d = start + timedelta(days=i)
        w = get_weather_features(d)
        for hour in (9, 11, 14, 17, 19):
            x = _vectorize(d, hour, w["temp_avg"], w["precip_prob"], w["is_weekend"])
            # Regla sintética: más no-show con lluvia alta, tarde-noche y fines de semana
            p = 0.1
            p += 0.4 if w["precip_prob"] > 0.4 else 0
            p += 0.15 if hour >= 17 else 0
            p += 0.1 if w["is_weekend"] == 1 else 0
            p = min(max(p, 0.01), 0.95)
            y_val = 1 if np.random.rand() < p else 0  # 1 => no-show
            X.append(x)
            y.append(y_val)
    return np.vstack(X), np.array(y)


def train_noshow_model() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    X, y = _synth_data()
    clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    clf.fit(X, y)
    joblib.dump(clf, MODEL_PATH)


def load_noshow_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


def predict_noshow(day: date, hour: int) -> Tuple[str, float]:
    model = load_noshow_model()
    w = get_weather_features(day)
    x = _vectorize(day, hour, w["temp_avg"], w["precip_prob"], w["is_weekend"])
    if model is None:
        # fallback simple por reglas
        p = 0.1
        p += 0.4 if w["precip_prob"] > 0.4 else 0
        p += 0.15 if hour >= 17 else 0
        p += 0.1 if w["is_weekend"] == 1 else 0
        p = float(min(max(p, 0.01), 0.95))
        return ("no-show" if p >= 0.5 else "show"), (p if p >= 0.5 else 1 - p)

    proba = float(model.predict_proba([x])[0][1])  # probabilidad de no-show
    label = "no-show" if proba >= 0.5 else "show"
    prob = proba if label == "no-show" else 1 - proba
    return label, prob


if __name__ == "__main__":
    train_noshow_model()
