

from fastapi.testclient import TestClient
from scoring.fastapi_app import app

client = TestClient(app)

def test_read_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert "customer_id" in response.json()[0]