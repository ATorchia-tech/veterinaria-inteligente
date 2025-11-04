from fastapi.testclient import TestClient
from app.main import app
from app.ml.intent import train_and_save_default


# Garantizar que el modelo esté entrenado
train_and_save_default()

client = TestClient(app)


def test_intent_top3_present_and_sorted():
    res = client.post("/ai/intent", json={"text": "Quiero agendar un turno para mañana"})
    assert res.status_code == 200
    data = res.json()
    assert "top3" in data
    assert isinstance(data["top3"], list)
    assert 1 <= len(data["top3"]) <= 3
    # Probabilidades dentro de [0,1] y ordenadas desc
    probs = [item["probability"] for item in data["top3"]]
    assert all(0.0 <= p <= 1.0 for p in probs)
    assert probs == sorted(probs, reverse=True)
    # La primera etiqueta coincide con la principal
    assert data["top3"][0]["label"] == data["label"]
