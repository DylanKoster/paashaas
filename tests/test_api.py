from freezegun import freeze_time
from datetime import datetime, timedelta
import httpx
import time
# import auth

# BASE_URL = "https://hy2ek84ac1.execute-api.eu-central-1.amazonaws.com/Prod"
BASE_URL = "http://localhost:3000"
DEFAULT_TIMEOUT = 120

def test_create_store():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "teststore"
    assert data["location"] == "testloc"
    assert "id" in data

def test_get_store():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{store_id}", timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == store_id
    assert data["name"] == "teststore"
    assert data["location"] == "testloc"

def test_update_store():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    response = httpx.put(BASE_URL + f"/stores/{store_id}", json={"name": "newname", "location": "newloc"}, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == store_id
    assert data["name"] == "newname"
    assert data["location"] == "newloc"

def test_create_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10}, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["store_id"] == store_id
    assert data["name"] == "Test Item"
    assert data["quantity"] == 10

def test_get_items():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    httpx.post(BASE_URL + f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10}, timeout=DEFAULT_TIMEOUT)

    response = httpx.get(BASE_URL + f"/stores/{store_id}/items/", timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["store_id"] == store_id

def test_get_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]
    response = httpx.post(BASE_URL + f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10}, timeout=DEFAULT_TIMEOUT)
    item_id = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{store_id}/items/{item_id}", timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["store_id"] == store_id
    assert data["name"] == "Test Item"

def test_update_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]
    response = httpx.post(BASE_URL + f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10}, timeout=DEFAULT_TIMEOUT)
    item_id = response.json()["id"]

    response = httpx.put(BASE_URL + f"/stores/{store_id}/items/{item_id}", json={"name": "New Item", "img": "", "quantity": 5}, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "New Item"
    assert data["quantity"] == 5

def test_create_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{store_id}/orders/", json={"items": [], "status": "pending"}, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["store_id"] == store_id
    assert data["status"] == "pending"

def test_get_orders():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    httpx.post(BASE_URL + f"/stores/{store_id}/orders/", json={"items": [], "status": "pending"}, timeout=DEFAULT_TIMEOUT)

    response = httpx.get(BASE_URL + f"/stores/{store_id}/orders/", timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["store_id"] == store_id

def test_get_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{store_id}/orders/", json={"items": [], "status": "pending"}, timeout=DEFAULT_TIMEOUT)
    order_id = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{store_id}/orders/{order_id}", timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["store_id"] == store_id
    assert data["status"] == "pending"

def test_complete_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{store_id}/orders/", json={"items": []}, timeout=DEFAULT_TIMEOUT)
    order_id = response.json()["id"]

    response = httpx.put(BASE_URL + f"/stores/{store_id}/orders/{order_id}", json={"status": "completed"}, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

def test_reserve_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"}, timeout=DEFAULT_TIMEOUT)
    store_id = response.json()["id"]
    print(response.json())

    response = httpx.post(BASE_URL + f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10}, timeout=DEFAULT_TIMEOUT)
    item_id = response.json()["id"]
    print(response.json())

    response = httpx.post(BASE_URL + f"/stores/{store_id}/orders/", json={"items": [{"item_id": item_id, "quantity": 5}]}, timeout=DEFAULT_TIMEOUT)
    order_id = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{store_id}/items/{item_id}", timeout=DEFAULT_TIMEOUT)
    print(response.json())
    data = response.json()
    assert data["quantity"] == 5

# def test_cancel_order():
#     response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
#     store_id = response.json()["id"]

#     response = httpx.post(BASE_URL + f"/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
#     item_id = response.json()["id"]

#     response = httpx.post(BASE_URL + f"/stores/{store_id}/orders/", json={"items": [{"item_id": item_id, "quantity": 5}]})
#     order_id = response.json()["id"]

#     response = httpx.get(BASE_URL + f"/stores/{store_id}/items/{item_id}")
#     data = response.json()
#     assert data["quantity"] == 5

#     time.sleep(70)

#     with freeze_time(datetime.now() + timedelta(minutes=20)):
#         response = httpx.get(BASE_URL + f"/stores/{store_id}/orders/{order_id}")
#         assert response.status_code == 200
#         data = response.json()
#         print(datetime.now())
#         print(data)
#         assert data["status"] == "cancelled"

#         response = httpx.get(BASE_URL + f"/stores/{store_id}/items/{item_id}")
#         data = response.json()
#         assert data["quantity"] == 10
