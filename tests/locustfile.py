from locust import HttpUser, task, between
import json

BASE_URL = "https://bgwljg4yk7.execute-api.eu-west-1.amazonaws.com/Prod"

class StoreUser (HttpUser ):
    wait_time = between(1, 3)

    @task(1)
    def create_store(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    @task(2)
    def get_store(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        store_id = response.json()["id"]

        response = self.client.get(f"{BASE_URL}/stores/{store_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id

    @task(3)
    def update_store(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        store_id = response.json()["id"]

        response = self.client.put(f"{BASE_URL}/stores/{store_id}", json={"name": "newname", "location": "newloc"})
        assert response.status_code == 200

    @task(4)
    def create_item(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        store_id = response.json()["id"]

        response = self.client.post(f"{BASE_URL}/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})
        assert response.status_code == 200

    @task(5)
    def get_items(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        store_id = response.json()["id"]

        self.client.post(f"{BASE_URL}/stores/{store_id}/items/", json={"name": "Test Item", "img": "", "quantity": 10})

        response = self.client.get(f"{BASE_URL}/stores/{store_id}/items/")
        assert response.status_code == 200

    @task(6)
    def create_order(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        store_id = response.json()["id"]

        response = self.client.post(f"{BASE_URL}/stores/{store_id}/orders/", json={"items": [], "status": "pending"})
        assert response.status_code == 200
