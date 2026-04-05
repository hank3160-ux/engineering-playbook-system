"""
URL Checker — /url-checker/check endpoint 測試。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient
from demo.main import app

client = TestClient(app)


def _post(url: str) -> dict:
    return client.post("/url-checker/check", json={"url": url}).json()


def test_https_url_is_secure() -> None:
    data = _post("https://example.com")
    assert data["is_https"] is True
    assert "Secure" in data["message"]


def test_http_url_is_insecure() -> None:
    data = _post("http://example.com")
    assert data["is_https"] is False
    assert "Insecure" in data["message"]


def test_response_contains_original_url() -> None:
    url = "https://github.com"
    data = _post(url)
    assert data["url"] == url


def test_empty_string_is_insecure() -> None:
    data = _post("")
    assert data["is_https"] is False


def test_https_uppercase_is_insecure() -> None:
    """協定大小寫不符合規範，視為不安全。"""
    data = _post("HTTPS://example.com")
    assert data["is_https"] is False


def test_status_code_200() -> None:
    response = client.post("/url-checker/check", json={"url": "https://example.com"})
    assert response.status_code == 200
