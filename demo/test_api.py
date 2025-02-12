import pytest
from fastapi.testclient import TestClient
from api import app
from models import Store, Item, InventoryItem, Order
from freezegun import freeze_time
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_store():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "teststore"
    assert data["location"] == "testloc"
    assert "_id" in data

def test_get_stores():
    response = client.get("/stores/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_store():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.get(f"/stores/{store_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == store_id
    assert data["name"] == "teststore"
    assert data["location"] == "testloc"

def test_update_store():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.put(f"/stores/{store_id}", json={"name": "newname", "location": "newloc"})
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == store_id
    assert data["name"] == "newname"
    assert data["location"] == "newloc"

def test_create_item():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.post(f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["store_id"] == store_id
    assert data["name"] == "Test Item"
    assert data["quantity"] == 10

def test_get_items():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    client.post(f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})

    response = client.get(f"/stores/{store_id}/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["store_id"] == store_id

def test_get_item():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]
    response = client.post(f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    item_id = response.json()["_id"]

    response = client.get(f"/stores/{store_id}/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == item_id
    assert data["store_id"] == store_id
    assert data["name"] == "Test Item"

def test_update_item():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]
    response = client.post(f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    item_id = response.json()["_id"]

    response = client.put(f"/stores/{store_id}/items/{item_id}", json={"name": "New Item", "quantity": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == item_id
    assert data["name"] == "New Item"
    assert data["quantity"] == 5

def test_create_order():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.post(f"/stores/{store_id}/orders/", json={"items": [], "status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert data["store_id"] == store_id
    assert data["status"] == "pending"

def test_get_orders():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    client.post(f"/stores/{store_id}/orders/", json={"items": [], "status": "pending"})

    response = client.get(f"/stores/{store_id}/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["store_id"] == store_id

def test_get_order():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.post(f"/stores/{store_id}/orders/", json={"items": [], "status": "pending"})
    order_id = response.json()["_id"]

    response = client.get(f"/stores/{store_id}/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == order_id
    assert data["store_id"] == store_id
    assert data["status"] == "pending"

def test_complete_order():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.post(f"/stores/{store_id}/orders/", json={"items": []})
    order_id = response.json()["_id"]

    response = client.put(f"/stores/{store_id}/orders/{order_id}", json={"status": "completed"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

def test_reserve_item():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]
    print(response.json())

    response = client.post(f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    item_id = response.json()["_id"]
    print(response.json())

    response = client.post(f"/stores/{store_id}/orders/", json={"items": [{"item_id": item_id, "quantity": 5}]})
    order_id = response.json()["_id"]
    print(response.json())

    response = client.get(f"/stores/{store_id}/items/{item_id}")
    print(response.json())
    data = response.json()
    assert data["quantity"] == 5

def test_cancel_order():
    response = client.post("/stores/", json={"name": "teststore", "location": "testloc"})
    store_id = response.json()["_id"]

    response = client.post(f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    item_id = response.json()["_id"]

    response = client.post(f"/stores/{store_id}/orders/", json={"items": [{"item_id": item_id, "quantity": 5}]})
    order_id = response.json()["_id"]

    response = client.get(f"/stores/{store_id}/items/{item_id}")
    data = response.json()
    assert data["quantity"] == 5

    with freeze_time(datetime.now() + timedelta(minutes=20)):
        response = client.get(f"/stores/{store_id}/orders/{order_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"

