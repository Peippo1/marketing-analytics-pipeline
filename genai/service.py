from __future__ import annotations

from datetime import datetime, UTC

from genai.brief_parser import slugify_campaign_name
from genai.copy_generator import MockCampaignGenerator, get_campaign_generator
from genai.schemas import CampaignBrief, CampaignManifest
from genai.storage import CampaignStorage


class CampaignBriefService:
    def __init__(self, storage: CampaignStorage | None = None):
        self.storage = storage or CampaignStorage()

    def generate_and_save(self, brief: CampaignBrief) -> CampaignManifest:
        generator = get_campaign_generator()
        try:
            output = generator.generate(brief)
            provider_name = generator.provider_name
            mode = generator.mode
        except Exception:
            fallback = MockCampaignGenerator()
            output = fallback.generate(brief)
            provider_name = fallback.provider_name
            mode = "fallback-mock"

        base_name = brief.campaign_name or brief.product_name or "campaignforge-brief"
        timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        campaign_id = f"{slugify_campaign_name(base_name)}-{timestamp}"
        return self.storage.save(campaign_id, provider_name, mode, brief, output)

    def load_campaign(self, campaign_id: str) -> CampaignManifest | None:
        return self.storage.load(campaign_id)

