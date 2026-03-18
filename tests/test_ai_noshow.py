from datetime import date
from fastapi.testclient import TestClient
from app.main import app
from app.ml.noshow import train_noshow_model

client = TestClient(app)


def setup_module():
    # train model only if it doesn't exist (avoid network calls during tests)
    from pathlib import Path

    model_path = (
        Path(__file__).resolve().parent.parent
        / "app"
        / "ml"
        / "models"
        / "noshow.joblib"
    )
    if not model_path.exists():
        train_noshow_model()


def test_noshow_endpoint():
    d = date.today().isoformat()
    res = client.get(f"/ai/noshow?day={d}&hour=17")
    assert res.status_code == 200
    data = res.json()
    assert data["label"] in ("no-show", "show")
    assert 0.0 <= data["probability"] <= 1.0
