
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


def test_generate_campaign_brief():
    response = client.post(
        "/genai/brief",
        json={
            "campaign_name": "API Launch",
            "product_name": "CampaignForge AI",
            "brief": "Launch CampaignForge AI to teams that need reusable campaign messaging and prompt-ready planning outputs.",
            "target_market": "startup marketing teams",
            "channels": ["LinkedIn", "Email"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["campaign_id"].startswith("api-launch-")
    assert payload["output"]["angles"]


def test_get_missing_campaign_returns_404():
    response = client.get("/genai/campaigns/does-not-exist")
    assert response.status_code == 404
