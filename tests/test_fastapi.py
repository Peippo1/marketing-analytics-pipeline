
from fastapi.testclient import TestClient
from scoring.fastapi_app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["x-content-type-options"] == "nosniff"


def test_read_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert "customer_id" in response.json()[0]


def test_customers_limit_is_bounded():
    response = client.get("/customers", params={"limit": 101})
    assert response.status_code == 422
