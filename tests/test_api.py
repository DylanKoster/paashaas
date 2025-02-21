from freezegun import freeze_time
from datetime import datetime, timedelta
import httpx

BASE_URL = "https://acovzz13a1.execute-api.eu-west-1.amazonaws.com/Prod"

def test_create_store():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "teststore"
    assert data["location"] == "testloc"
    assert "id" in data

def test_get_store():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{storeid}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == storeid
    assert data["name"] == "teststore"
    assert data["location"] == "testloc"

def test_update_store():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.put(BASE_URL + f"/stores/{storeid}", json={"name": "newname", "location": "newloc"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == storeid
    assert data["name"] == "newname"
    assert data["location"] == "newloc"

def test_create_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{storeid}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["storeid"] == storeid
    assert data["name"] == "Test Item"
    assert data["quantity"] == 10

def test_get_items():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    httpx.post(BASE_URL + f"/stores/{storeid}/items/", json={"name": "Test Item", "img": "", "quantity": 10})

    response = httpx.get(BASE_URL + f"/stores/{storeid}/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["storeid"] == storeid

def test_get_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]
    response = httpx.post(BASE_URL + f"/stores/{storeid}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    itemid = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{storeid}/items/{itemid}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == itemid
    assert data["storeid"] == storeid
    assert data["name"] == "Test Item"

def test_update_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]
    response = httpx.post(BASE_URL + f"/stores/{storeid}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    itemid = response.json()["id"]

    response = httpx.put(BASE_URL + f"/stores/{storeid}/items/{itemid}", json={"name": "New Item", "quantity": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == itemid
    assert data["name"] == "New Item"
    assert data["quantity"] == 5

def test_create_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{storeid}/orders/", json={"items": [], "status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert data["storeid"] == storeid
    assert data["status"] == "pending"

def test_get_orders():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    httpx.post(BASE_URL + f"/stores/{storeid}/orders/", json={"items": [], "status": "pending"})

    response = httpx.get(BASE_URL + f"/stores/{storeid}/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["storeid"] == storeid

def test_get_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{storeid}/orders/", json={"items": [], "status": "pending"})
    orderid = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{storeid}/orders/{orderid}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == orderid
    assert data["storeid"] == storeid
    assert data["status"] == "pending"

def test_complete_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{storeid}/orders/", json={"items": []})
    orderid = response.json()["id"]

    response = httpx.put(BASE_URL + f"/stores/{storeid}/orders/{orderid}", json={"status": "completed"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

def test_reserve_item():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]
    print(response.json())

    response = httpx.post(BASE_URL + f"/stores/{storeid}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    itemid = response.json()["id"]
    print(response.json())

    response = httpx.post(BASE_URL + f"/stores/{storeid}/orders/", json={"items": [{"itemid": itemid, "quantity": 5}]})
    orderid = response.json()["id"]
    print(response.json())

    response = httpx.get(BASE_URL + f"/stores/{storeid}/items/{itemid}")
    print(response.json())
    data = response.json()
    assert data["quantity"] == 5

def test_cancel_order():
    response = httpx.post(BASE_URL + "/stores/", json={"name": "teststore", "location": "testloc"})
    storeid = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{storeid}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
    itemid = response.json()["id"]

    response = httpx.post(BASE_URL + f"/stores/{storeid}/orders/", json={"items": [{"itemid": itemid, "quantity": 5}]})
    orderid = response.json()["id"]

    response = httpx.get(BASE_URL + f"/stores/{storeid}/items/{itemid}")
    data = response.json()
    assert data["quantity"] == 5

    with freeze_time(datetime.now() + timedelta(minutes=20)):
        response = httpx.get(BASE_URL + f"/stores/{storeid}/orders/{orderid}")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"
