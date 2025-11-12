from typing import Tuple
import numpy as np
from app.ml.model import load_model
from app.ml.features import vectorize

LABELS = {0: "Baja", 1: "Media", 2: "Alta"}


def predict_affluence(features: dict) -> Tuple[str, float]:
    model = load_model()
    if model is None:
        # Si no hay modelo entrenado, decidir por regla simple
        x = vectorize(features)
        score = 0
        if x[2] == 1 and x[0] > 18 and x[1] < 0.2:
            label = "Alta"
            prob = 0.7
        elif x[1] > 0.25:
            label = "Baja"
            prob = 0.6
        else:
            label = "Media"
            prob = 0.5
        return label, float(prob)

    x = np.array([vectorize(features)])
    proba = model.predict_proba(x)[0]
    idx = int(np.argmax(proba))
    return LABELS.get(idx, "Media"), float(proba[idx])
