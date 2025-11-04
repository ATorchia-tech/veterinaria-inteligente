from fastapi.testclient import TestClient
from app.main import app
from app.ml.sentiment import train_sentiment_model

client = TestClient(app)


def setup_module():
    # ensure model exists
    train_sentiment_model()


def test_sentiment_positive():
    res = client.post("/ai/sentiment", json={"text": "excelente servicio y atención"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] in ("positivo", "negativo")
    assert 0.0 <= data["probability"] <= 1.0


def test_sentiment_negative():
    res = client.post("/ai/sentiment", json={"text": "pésimo y muy mala experiencia"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] in ("positivo", "negativo")
    assert 0.0 <= data["probability"] <= 1.0
