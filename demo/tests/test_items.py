"""
Items CRUD — /items endpoint 測試。
示範通用 CRUD 的完整測試覆蓋。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from fastapi.testclient import TestClient
from demo.main import app
from demo.services import item_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store() -> None:
    """每個測試前重置 in-memory store，確保測試隔離。"""
    item_service._store.clear()
    item_service._next_id = 1


def test_create_item() -> None:
    response = client.post("/items/", json={"name": "Widget", "description": "A test widget"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Widget"


def test_list_items_empty() -> None:
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_after_create() -> None:
    client.post("/items/", json={"name": "Alpha"})
    client.post("/items/", json={"name": "Beta"})
    response = client.get("/items/")
    assert len(response.json()) == 2


def test_get_item_by_id() -> None:
    client.post("/items/", json={"name": "Gamma"})
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Gamma"


def test_get_nonexistent_item_returns_404() -> None:
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_delete_item() -> None:
    client.post("/items/", json={"name": "ToDelete"})
    response = client.delete("/items/1")
    assert response.status_code == 204
    assert client.get("/items/1").status_code == 404


def test_delete_nonexistent_item_returns_404() -> None:
    response = client.delete("/items/999")
    assert response.status_code == 404
