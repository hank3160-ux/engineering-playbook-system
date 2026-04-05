"""
範例測試 — /health endpoint。
執行：pytest tests/ -v
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_contains_required_fields() -> None:
    data = client.get("/health").json()
    for field in ("status", "service", "version", "uptime_seconds", "timestamp"):
        assert field in data, f"Missing field: {field}"


def test_health_process_time_header() -> None:
    response = client.get("/health")
    assert "x-process-time-ms" in response.headers
