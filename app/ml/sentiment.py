from __future__ import annotations
from pathlib import Path
from typing import Tuple

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

MODELS_DIR = Path(__file__).resolve().parent / "models"
SENTIMENT_PATH = MODELS_DIR / "sentiment.joblib"


def _default_training_data():
    positives = [
        "excelente servicio",
        "muy buena atención",
        "todo perfecto",
        "recomiendo esta veterinaria",
        "trato amable y profesional",
        "rápidos y eficientes",
        "mi mascota quedó feliz",
    ]
    negatives = [
        "muy mala experiencia",
        "pésimo servicio",
        "no lo recomiendo",
        "lentos y desorganizados",
        "trato desagradable",
        "caro y deficiente",
        "mi mascota salió peor",
    ]
    X = positives + negatives
    y = [1] * len(positives) + [0] * len(negatives)
    return X, y


def train_sentiment_model() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    X, y = _default_training_data()
    pipe: Pipeline = Pipeline(
        [
            ("vec", CountVectorizer(ngram_range=(1, 2), lowercase=True)),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000, class_weight="balanced", random_state=42
                ),
            ),
        ]
    )
    pipe.fit(X, y)
    joblib.dump(pipe, SENTIMENT_PATH)


def load_sentiment_model():
    if SENTIMENT_PATH.exists():
        return joblib.load(SENTIMENT_PATH)
    return None


def predict_sentiment(text: str) -> Tuple[str, float]:
    model = load_sentiment_model()
    if model is None:
        # train once on the fly for convenience
        train_sentiment_model()
        model = load_sentiment_model()

    proba = model.predict_proba([text])[0]
    idx_positive = 1  # label 1 => positivo
    p_pos = float(proba[idx_positive])
    label = "positivo" if p_pos >= 0.5 else "negativo"
    return label, p_pos if label == "positivo" else 1.0 - p_pos


if __name__ == "__main__":
    train_sentiment_model()
