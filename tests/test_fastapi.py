

from fastapi.testclient import TestClient
from api.main import app  # assuming your FastAPI app is in api/main.py

client = TestClient(app)

def test_read_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert "customer_id" in response.json()[0]