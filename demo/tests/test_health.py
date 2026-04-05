"""
Demo — /health endpoint 測試。
執行：pytest demo/tests/ -v
"""

import sys
import os

# 確保 demo 套件可被 import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient
from demo.main import app

client = TestClient(app)


def test_health_status_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_contains_required_fields() -> None:
    data = client.get("/health").json()
    for field in ("status", "version", "uptime_seconds", "timestamp"):
        assert field in data, f"Missing field: {field}"


def test_health_process_time_header() -> None:
    """ProcessTimeMiddleware 應在 Response Header 中注入 X-Process-Time-Ms。"""
    response = client.get("/health")
    assert "x-process-time-ms" in response.headers


def test_unhandled_exception_returns_json() -> None:
    """不存在的路由應回傳 JSON 而非 HTML。"""
    response = client.get("/this-route-does-not-exist")
    assert response.status_code == 404
    # FastAPI 預設 404 已是 JSON
    assert response.headers["content-type"].startswith("application/json")
