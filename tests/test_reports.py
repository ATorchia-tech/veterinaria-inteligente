from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.main import app
from app.db import seed

client = TestClient(app)


def setup_module():
    seed.seed()


def test_attendance_report():
    start = date.today() - timedelta(days=1)
    end = date.today() + timedelta(days=1)
    res = client.get(
        f"/reports/attendance?start={start.isoformat()}&end={end.isoformat()}"
    )
    assert res.status_code == 200
    data = res.json()
    assert set(data.keys()) == {"start", "end", "attended", "canceled", "scheduled"}
