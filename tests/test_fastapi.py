
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
            "brief": (
                "Launch CampaignForge AI to teams that need reusable campaign "
                "messaging and prompt-ready planning outputs."
            ),
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


def test_list_campaigns_endpoint():
    response = client.get("/genai/campaigns")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_generate_campaign_images():
    campaign_response = client.post(
        "/genai/brief",
        json={
            "campaign_name": "Image API Launch",
            "product_name": "CampaignForge AI",
            "brief": (
                "Generate campaign angles and image prompts for a polished "
                "product launch demo."
            ),
        },
    )
    campaign_id = campaign_response.json()["campaign_id"]
    angle_id = campaign_response.json()["output"]["angles"][0]["angle_id"]

    response = client.post(
        "/genai/images",
        json={
            "campaign_id": campaign_id,
            "angle_id": angle_id,
            "style": "Campaign concept board",
            "count": 2,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["campaign_id"] == campaign_id
    assert len(payload["assets"]) == 2

    read_response = client.get(f"/genai/campaigns/{campaign_id}/images")
    assert read_response.status_code == 200
    filename = payload["assets"][0]["file_path"].split("/")[-1]

    asset_response = client.get(f"/genai/assets/{campaign_id}/{filename}")
    assert asset_response.status_code == 200
    assert asset_response.headers["content-type"].startswith("image/")


def test_get_campaign_images_returns_404_when_missing():
    response = client.get("/genai/campaigns/does-not-exist/images")
    assert response.status_code == 404


def test_review_and_export_campaign_workflow():
    campaign_response = client.post(
        "/genai/brief",
        json={
            "campaign_name": "Workflow API Launch",
            "product_name": "CampaignForge AI",
            "brief": (
                "Create a workflow-ready campaign with approval and export "
                "support."
            ),
        },
    )
    campaign_id = campaign_response.json()["campaign_id"]
    angle_id = campaign_response.json()["output"]["angles"][0]["angle_id"]

    regenerate_response = client.post(
        f"/genai/campaigns/{campaign_id}/regenerate",
        json={"scope": "copy"},
    )
    assert regenerate_response.status_code == 200

    image_response = client.post(
        "/genai/images",
        json={
            "campaign_id": campaign_id,
            "angle_id": angle_id,
            "count": 1,
        },
    )
    image_id = image_response.json()["assets"][0]["image_id"]

    review_response = client.post(
        f"/genai/campaigns/{campaign_id}/images/review",
        json={"image_id": image_id, "approval_status": "approved"},
    )
    assert review_response.status_code == 200
    assert review_response.json()["assets"][0]["approval_status"] == "approved"

    export_response = client.get(f"/genai/campaigns/{campaign_id}/export")
    assert export_response.status_code == 200
    assert export_response.headers["content-type"].startswith("application/zip")
