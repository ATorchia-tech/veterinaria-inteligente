from pathlib import Path
import joblib

MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "affluence_model.pkl"


def save_model(model) -> None:
    joblib.dump(model, MODEL_PATH)


def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None
