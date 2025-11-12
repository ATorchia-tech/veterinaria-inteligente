from fastapi.testclient import TestClient
from app.main import app
from app.ml.intent import train_and_save_default


# Entrenar el modelo una vez antes de las pruebas
train_and_save_default()

client = TestClient(app)


def test_intent_turnos():
    res = client.post(
        "/ai/intent", json={"text": "Quiero agendar un turno para mañana"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "turnos"
    assert 0.0 <= data["probability"] <= 1.0


def test_intent_vacunacion():
    res = client.post(
        "/ai/intent", json={"text": "Necesito el refuerzo de la vacuna antirrábica"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "vacunacion"


def test_intent_emergencia():
    res = client.post("/ai/intent", json={"text": "Es una emergencia, está sangrando"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "emergencia"


def test_intent_precios_o_servicios():
    res = client.post(
        "/ai/intent", json={"text": "Cuál es el precio de la castración?"}
    )
    assert res.status_code == 200
    data = res.json()
    # según dataset, debería clasificar como precios (incluye 'precio')
    assert data["label"] in ("precios", "servicios")


def test_intent_horarios():
    res = client.post("/ai/intent", json={"text": "Qué horarios tienen los domingos?"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "horarios"
