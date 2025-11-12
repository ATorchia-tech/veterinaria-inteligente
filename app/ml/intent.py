from __future__ import annotations

import os
import unicodedata
from typing import Tuple, Dict, Any, List

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)
import json


MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "intent.joblib")
DEFAULT_DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "data", "intent_samples.csv"
)
METRICS_JSON_PATH = os.path.join(MODEL_DIR, "intent_metrics.json")
CM_CSV_PATH = os.path.join(MODEL_DIR, "intent_confusion_matrix.csv")


def _strip_accents(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def build_pipeline() -> Pipeline:
    # Preprocesa acentos usando preprocessor de TfidfVectorizer (función global picklable)
    vect = TfidfVectorizer(
        ngram_range=(1, 2), min_df=1, preprocessor=_strip_accents, lowercase=False
    )
    clf = LogisticRegression(max_iter=1000, n_jobs=None)
    pipe = Pipeline(
        [
            ("tfidf", vect),
            ("clf", clf),
        ]
    )
    return pipe


def train_from_csv(csv_path: str = DEFAULT_DATASET_PATH) -> Pipeline:
    df = pd.read_csv(csv_path)
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV debe contener columnas 'text' y 'label'")
    X = df["text"].astype(str).tolist()
    y = df["label"].astype(str).tolist()

    pipe = build_pipeline()
    pipe.fit(X, y)
    return pipe


def _compute_cv_metrics(
    X: List[str], y: List[str], n_splits: int = 5, random_state: int = 42
) -> Dict[str, Any]:
    labels = sorted(list(set(y)))
    # Ajustar n_splits según el mínimo de ejemplos por clase
    from collections import Counter

    counts = Counter(y)
    min_count = min(counts.values()) if counts else 0
    eff_splits = max(2, min(n_splits, min_count)) if min_count >= 2 else 0

    pipe = build_pipeline()
    if eff_splits >= 2:
        skf = StratifiedKFold(
            n_splits=eff_splits, shuffle=True, random_state=random_state
        )
        # Predicciones por validación cruzada (evita fuga de datos)
        y_pred = cross_val_predict(pipe, X, y, cv=skf)
        cv_used = True
    else:
        # Fallback: hold-out simple si no se puede estratificar
        X_tr, X_te, y_tr, y_te = train_test_split(
            X,
            y,
            test_size=0.33,
            random_state=random_state,
            stratify=y if len(labels) > 1 else None,
        )
        pipe.fit(X_tr, y_tr)
        y_pred = pipe.predict(X_te)
        # Para unificar métricas, comparamos sobre test solamente
        X, y = X_te, y_te
        cv_used = False

    acc = accuracy_score(y, y_pred)
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(
        y, y_pred, average="macro", zero_division=0
    )
    prec_micro, rec_micro, f1_micro, _ = precision_recall_fscore_support(
        y, y_pred, average="micro", zero_division=0
    )
    prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y, y_pred, average="weighted", zero_division=0
    )

    # métricas por clase
    prec_cls, rec_cls, f1_cls, _ = precision_recall_fscore_support(
        y, y_pred, labels=labels, zero_division=0
    )
    per_class = {
        lbl: {
            "precision": float(prec_cls[i]),
            "recall": float(rec_cls[i]),
            "f1": float(f1_cls[i]),
        }
        for i, lbl in enumerate(labels)
    }

    cm = confusion_matrix(y, y_pred, labels=labels)

    result = {
        "labels": labels,
        "cv_used": cv_used,
        "cv_n_splits": int(eff_splits) if cv_used else None,
        "accuracy_cv": float(acc),
        "precision_macro_cv": float(prec_macro),
        "recall_macro_cv": float(rec_macro),
        "f1_macro_cv": float(f1_macro),
        "precision_micro_cv": float(prec_micro),
        "recall_micro_cv": float(rec_micro),
        "f1_micro_cv": float(f1_micro),
        "precision_weighted_cv": float(prec_weighted),
        "recall_weighted_cv": float(rec_weighted),
        "f1_weighted_cv": float(f1_weighted),
        "per_class_cv": per_class,
        "confusion_matrix_cv": cm.tolist(),
    }
    return result


def _save_metrics_artifacts(
    metrics: Dict[str, Any],
    metrics_path: str = METRICS_JSON_PATH,
    cm_csv_path: str = CM_CSV_PATH,
) -> None:
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    # Guardar JSON con métricas
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    # Guardar CM también en CSV con encabezados
    labels = metrics.get("labels", [])
    cm = metrics.get("confusion_matrix_cv", [])
    df_cm = pd.DataFrame(cm, index=labels, columns=labels)
    df_cm.to_csv(cm_csv_path, index=True, encoding="utf-8")


def save_model(pipe: Pipeline, path: str = MODEL_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(pipe, path)


def load_model(path: str = MODEL_PATH) -> Pipeline:
    return joblib.load(path)


def predict_intent(text: str, path: str = MODEL_PATH) -> Tuple[str, float]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    pipe = load_model(path)
    proba = pipe.predict_proba([text])[0]
    idx = proba.argmax()
    label = pipe.classes_[idx]
    return str(label), float(proba[idx])


def predict_intent_topk(
    text: str, k: int = 3, path: str = MODEL_PATH
) -> List[Tuple[str, float]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    pipe = load_model(path)
    proba = pipe.predict_proba([text])[0]
    classes = list(pipe.classes_)
    # top-k indices sorted desc
    idxs = sorted(range(len(proba)), key=lambda i: proba[i], reverse=True)[: max(1, k)]
    return [(str(classes[i]), float(proba[i])) for i in idxs]


def train_and_save_default(
    csv_path: str = DEFAULT_DATASET_PATH, model_path: str = MODEL_PATH
) -> str:
    pipe = train_from_csv(csv_path)
    save_model(pipe, model_path)
    # Calcular y guardar métricas de validación cruzada con el dataset completo
    df = pd.read_csv(csv_path)
    X_all = df["text"].astype(str).tolist()
    y_all = df["label"].astype(str).tolist()
    metrics = _compute_cv_metrics(X_all, y_all, n_splits=5, random_state=42)
    _save_metrics_artifacts(metrics, METRICS_JSON_PATH, CM_CSV_PATH)
    return model_path


if __name__ == "__main__":
    # Entrena con el dataset por defecto y guarda el modelo
    model_path = train_and_save_default()
    print(f"Modelo entrenado y guardado en: {model_path}")
