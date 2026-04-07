from __future__ import annotations

from datetime import datetime, UTC

from genai.brief_parser import slugify_campaign_name
from genai.copy_generator import MockCampaignGenerator, get_campaign_generator
from genai.image_generator import MockImageGenerator, get_image_generator
from genai.schemas import CampaignBrief, CampaignManifest, ImageGenerationManifest, ImageGenerationRequest
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

    def list_campaigns(self) -> list[CampaignManifest]:
        return self.storage.list_campaigns()


class CampaignImageService:
    def __init__(self, storage: CampaignStorage | None = None):
        self.storage = storage or CampaignStorage()

    def generate_and_save(self, request: ImageGenerationRequest) -> ImageGenerationManifest:
        campaign = self.storage.load(request.campaign_id)
        if campaign is None:
            raise ValueError("Campaign output not found")

        selected_angle = None
        if request.angle_id:
            selected_angle = next((angle for angle in campaign.output.angles if angle.angle_id == request.angle_id), None)
            if selected_angle is None:
                raise ValueError("Campaign angle not found")

        prompt = request.prompt
        if not prompt:
            if selected_angle and selected_angle.image_prompts:
                prompt = selected_angle.image_prompts[0]
            else:
                raise ValueError("A prompt or valid angle_id is required")

        generator = get_image_generator()
        image_dir = self.storage.campaign_image_dir(request.campaign_id)
        try:
            assets = generator.generate(
                output_dir=image_dir,
                campaign_id=request.campaign_id,
                prompt=prompt,
                style=request.style,
                count=request.count,
            )
            provider_name = generator.provider_name
            mode = generator.mode
        except Exception:
            fallback = MockImageGenerator()
            assets = fallback.generate(
                output_dir=image_dir,
                campaign_id=request.campaign_id,
                prompt=prompt,
                style=request.style,
                count=request.count,
            )
            provider_name = fallback.provider_name
            mode = "fallback-mock"

        relative_assets = [
            asset.model_copy(update={"file_path": str(Path(asset.file_path).resolve().relative_to(self.storage.repo_root.resolve()))})
            for asset in assets
        ]
        manifest = ImageGenerationManifest(
            campaign_id=request.campaign_id,
            angle_id=request.angle_id,
            created_at=datetime.now(UTC).isoformat(),
            provider=provider_name,
            mode=mode,
            style=request.style,
            prompt=prompt,
            assets=relative_assets,
        )
        return self.storage.save_image_manifest(manifest)

    def load_manifest(self, campaign_id: str) -> ImageGenerationManifest | None:
        return self.storage.load_image_manifest(campaign_id)
