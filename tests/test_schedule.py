from fastapi.testclient import TestClient
from datetime import date
from app.main import app
from app.db import seed

client = TestClient(app)


def setup_module():
    seed.seed()


def test_agenda_diaria_returns_appointments():
    today = date.today().isoformat()
    res = client.get(f"/schedule/day?day={today}")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) >= 1
