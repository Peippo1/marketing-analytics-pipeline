from pathlib import Path

from genai.schemas import CampaignBrief
from genai.service import CampaignBriefService
from genai.storage import CampaignStorage


def test_generate_and_save_campaign_brief(tmp_path: Path):
    service = CampaignBriefService(storage=CampaignStorage(root=tmp_path / "generated"))
    manifest = service.generate_and_save(
        CampaignBrief(
            campaign_name="Demo Launch",
            product_name="CampaignForge AI",
            brief=(
                "Launch CampaignForge AI to modern marketing teams that need "
                "structured messaging and prompt-ready outputs."
            ),
            target_market="modern marketing teams",
            channels=["LinkedIn", "Email"],
        )
    )

    assert manifest.campaign_id.startswith("demo-launch-")
    assert manifest.output.angles
    assert len(manifest.output.angles[0].headlines) == 5
    assert (tmp_path / "generated" / "manifests" / f"{manifest.campaign_id}.json").exists()
    assert (tmp_path / "generated" / "copy" / f"{manifest.campaign_id}.json").exists()
