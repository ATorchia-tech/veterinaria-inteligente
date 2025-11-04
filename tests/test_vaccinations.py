from fastapi.testclient import TestClient
from app.main import app
from app.db import seed

client = TestClient(app)


def setup_module():
    seed.seed()


def test_upcoming_vaccinations():
    res = client.get("/vaccinations/upcoming?days=30")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) >= 1
