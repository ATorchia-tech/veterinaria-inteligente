from sklearn.ensemble import RandomForestClassifier
import numpy as np
from datetime import date, timedelta
from app.ml.features import vectorize
from app.ml.model import save_model

# Entrenamiento con datos sintéticos para desbloquear el endpoint de IA


def synth_data(n_days: int = 365):
    X, y = [], []
    start = date.today() - timedelta(days=n_days)
    for i in range(n_days):
        d = start + timedelta(days=i)
        feats = {
            "date": d,
            "temp_avg": 10 + 15 * np.sin(2 * np.pi * d.timetuple().tm_yday / 365.0),
            "precip_prob": 0.3 if d.weekday() in (5, 6) else 0.1,
            "is_weekend": 1 if d.weekday() >= 5 else 0,
            "month": d.month,
            "weekday": d.weekday(),
        }
        X.append(vectorize(feats))
        # Regla simple: fines de semana y buen clima => Alta, lluvia => Baja
        if (
            feats["is_weekend"]
            and feats["temp_avg"] > 18
            and feats["precip_prob"] < 0.2
        ):
            y.append(2)  # Alta
        elif feats["precip_prob"] > 0.25:
            y.append(0)  # Baja
        else:
            y.append(1)  # Media
    return np.array(X), np.array(y)


def train_and_save():
    X, y = synth_data()
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    save_model(model)


if __name__ == "__main__":
    train_and_save()
