from fastapi.testclient import TestClient
from app.main import app
from app.db import seed

client = TestClient(app)


def setup_module():
    # populate DB with seed data
    seed.seed()


def test_create_and_list_record():
    res = client.get("/pets")
    assert res.status_code == 200
    pets = res.json()
    assert len(pets) > 0
    pet_id = pets[0]["id"]

    payload = {
        "pet_id": pet_id,
        "symptoms": "tos",
        "diagnosis": "gripe",
        "treatment": "reposo",
        "medications": "ninguna",
    }
    r = client.post("/records/", json=payload)
    assert r.status_code == 200
    rec = r.json()
    assert rec["pet_id"] == pet_id

    resp = client.get(f"/records?pet_id={pet_id}")
    assert resp.status_code == 200
    found = [x for x in resp.json() if x.get("id") == rec.get("id")]
    assert len(found) == 1
