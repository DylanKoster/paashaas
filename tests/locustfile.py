from locust import HttpUser, task, between
import json
import auth

# run with: locust -f locustfile.py -u 10 -r 10 --host=https://bgwljg4yk7.execute-api.eu-west-1.amazonaws.com

BASE_URL = "https://bgwljg4yk7.execute-api.eu-west-1.amazonaws.com/Prod"

class StoreUser (HttpUser ):
    wait_time = between(1, 3)

    @task(1)
    def create_store(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    @task(2)
    def get_store(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req2 = auth.signed_request("GET", f"{BASE_URL}/stores/{store_id}")
        response = self.client.get(f"{BASE_URL}/stores/{store_id}", headers=dict(req2.headers))
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == "teststore"
        assert data["location"] == "testloc"

    @task(3)
    def update_store(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req = auth.signed_request("PUT", f"{BASE_URL}/stores/{store_id}", {"name": "newname", "location": "newloc"})
        response = self.client.put(f"{BASE_URL}/stores/{store_id}", data=req.data, headers=dict(req.headers))
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == "newname"
        assert data["location"] == "newloc"

    @task(4)
    def create_item(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req = auth.signed_request("POST", f"{BASE_URL}/stores/{store_id}/items/", {"name": "Test Item", "img": "", "quantity": 10})
        response = self.client.post(f"{BASE_URL}/stores/{store_id}/items/", data=req.data, headers=dict(req.headers))
        item_id = response.json()["id"]

        assert response.status_code == 200
        data = response.json()
        assert data["store_id"] == store_id
        assert data["name"] == "Test Item"
        assert data["quantity"] == 10

    @task(5)
    def get_items(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req = auth.signed_request("POST", f"{BASE_URL}/stores/{store_id}/items/", {"name": "Test Item", "img": "", "quantity": 10})
        response = self.client.post(f"{BASE_URL}/stores/{store_id}/items/", data=req.data, headers=dict(req.headers))
        item_id = response.json()["id"]

        response = self.client.get(f"{BASE_URL}/stores/{store_id}/items/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["store_id"] == store_id

    @task(6)
    def get_item(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req = auth.signed_request("POST", f"{BASE_URL}/stores/{store_id}/items/", {"name": "Test Item", "img": "", "quantity": 10})
        response = self.client.post(f"{BASE_URL}/stores/{store_id}/items/", data=req.data, headers=dict(req.headers))
        item_id = response.json()["id"]

        response = self.client.get(f"{BASE_URL}/stores/{store_id}/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["store_id"] == store_id
        assert data["name"] == "Test Item"

    @task(7)
    def update_item(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req2 = auth.signed_request("POST", f"{BASE_URL}/stores/{store_id}/items/", {"name": "Test Item", "img": "", "quantity": 10})
        response = self.client.post(f"{BASE_URL}/stores/{store_id}/items/", data=req2.data, headers=dict(req2.headers))
        item_id = response.json()["id"]

        req3 = auth.signed_request("PUT", f"{BASE_URL}/stores/{store_id}/items/{item_id}", {"name": "New Item", "img": "", "quantity": 5})
        response = self.client.put(f"{ BASE_URL}/stores/{store_id}/items/{item_id}", data=req3.data, headers=dict(req3.headers))
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == "New Item"
        assert data["quantity"] == 5

    @task(8)
    def create_order(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        response = self.client.post(f"{BASE_URL}/stores/{store_id}/orders/", json={"items": [], "status": "pending"})
        assert response.status_code == 200
        data = response.json()
        assert data["store_id"] == store_id
        assert data["status"] == "pending"

    @task(9)
    def get_orders(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        self.client.post(f"{BASE_URL}/stores/{store_id}/orders/", json={"items": [], "status": "pending"})

        req2 = auth.signed_request("GET", f"{BASE_URL}/stores/{store_id}/orders/")
        response = self.client.get(f"{BASE_URL}/stores/{store_id}/orders/", headers=dict(req2.headers))
        # assert response.status_code == 200
        # TODO double check this response
        # data = response.json()
        # assert isinstance(data, list)
        # assert len(data) > 0
        # assert data[0]["store_id"] == store_id

    @task(10)
    def get_order(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        response = self.client.post(f"{BASE_URL}/stores/{store_id}/orders/", json={"items": [], "status": "pending"})
        order_id = response.json()["id"]

        response = self.client.get(f"{BASE_URL}/stores/{store_id}/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id
        assert data["store_id"] == store_id
        assert data["status"] == "pending"

    @task(11)
    def complete_order(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        response = self.client.post(f"{BASE_URL}/stores/{store_id}/orders/", json={"items": []})
        order_id = response.json()["id"]

        response = self.client.put(f"{BASE_URL}/stores/{store_id}/orders/{order_id}", json={"status": "completed"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"

    @task(12)
    def reserve_item(self):
        req = auth.signed_request("POST", f"{BASE_URL}/stores/", {"name": "teststore", "location": "testloc"})
        response = self.client.post(f"{BASE_URL}/stores/", data=req.data, headers=dict(req.headers))
        store_id = response.json()["id"]

        req = auth.signed_request("POST", f"{BASE_URL}/stores/{store_id}/items/", {"name": "Test Item", "img": "", "quantity": 10})
        response = self.client.post(f"{BASE_URL}/stores/{store_id}/items/", data=req.data, headers=dict(req.headers))
        item_id = response.json()["id"]

        response = self.client.post(f"{BASE_URL}/stores/{store_id}/orders/", json={"items": [{"item_id": item_id, "quantity": 5}]})
        order_id = response.json()["id"]

        response = self.client.get(f"{BASE_URL}/stores/{store_id}/items/{item_id}")
        data = response.json()
        assert data["quantity"] == 5
