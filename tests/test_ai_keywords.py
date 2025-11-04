from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_classify_turnos():
    res = client.post("/ai/classify", json={"text": "Quiero agendar un turno para mañana"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] in ("turnos", "emergencia", "vacunacion", "precios", "horarios", "servicios", "ubicacion", "contacto", "otros")
    # En este caso debería ser turnos
    assert data["label"] == "turnos"
    assert 0.0 <= data["confidence"] <= 1.0


def test_classify_vacunacion():
    res = client.post("/ai/classify", json={"text": "Necesito el refuerzo de la vacuna antirrábica"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "vacunacion"


def test_classify_emergencia():
    res = client.post("/ai/classify", json={"text": "Es una emergencia, está sangrando"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "emergencia"


def test_classify_precios():
    res = client.post("/ai/classify", json={"text": "¿Cuál es el precio de la castración?"})
    assert res.status_code == 200
    data = res.json()
    # puede clasificar como precios (palabra precio) o servicios (castracion)
    assert data["label"] in ("precios", "servicios")


def test_classify_horarios():
    res = client.post("/ai/classify", json={"text": "¿Qué horarios tienen los domingos?"})
    assert res.status_code == 200
    data = res.json()
    assert data["label"] == "horarios"
