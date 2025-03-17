from locust import HttpUser , task, between
import json

BASE_URL = "https://bgwljg4yk7.execute-api.eu-west-1.amazonaws.com/Prod/stores"

class StoreUser (HttpUser ):
    wait_time = between(1, 3)  # Simulate a wait time between requests

    @task(1)
    def create_store(self):
        response = self.client.post(f"{BASE_URL}/stores/", json={"name": "teststore", "location": "testloc"})
        assert response.status_code == 200
        data = response.json()
        assert "id" in data