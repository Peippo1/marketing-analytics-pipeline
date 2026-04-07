from __future__ import annotations

from datetime import datetime, UTC
import json
from pathlib import Path

from genai.schemas import CampaignManifest, CampaignOutput, ImageGenerationManifest, SavedArtifact


DEFAULT_GENERATED_ROOT = Path(__file__).resolve().parents[1] / "data" / "generated"


class CampaignStorage:
    def __init__(self, root: Path | None = None):
        self.root = root or DEFAULT_GENERATED_ROOT
        self.repo_root = self.root.parents[1]
        self.copy_dir = self.root / "copy"
        self.brief_dir = self.root / "briefs"
        self.prompt_dir = self.root / "prompts"
        self.image_dir = self.root / "images"
        self.manifest_dir = self.root / "manifests"
        self.export_dir = self.root / "exports"
        for directory in (self.copy_dir, self.brief_dir, self.prompt_dir, self.image_dir, self.manifest_dir, self.export_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def save(self, campaign_id: str, provider: str, mode: str, brief, output: CampaignOutput) -> CampaignManifest:
        copy_path = self.copy_dir / f"{campaign_id}.json"
        brief_path = self.brief_dir / f"{campaign_id}.json"
        prompts_path = self.prompt_dir / f"{campaign_id}.json"
        manifest_path = self.manifest_dir / f"{campaign_id}.json"

        payload = output.model_dump(mode="json")
        copy_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        brief_path.write_text(brief.model_dump_json(indent=2), encoding="utf-8")
        prompts_payload = {
            "campaign_id": campaign_id,
            "angles": [
                {
                    "angle_id": angle.angle_id,
                    "title": angle.title,
                    "image_prompts": angle.image_prompts,
                }
                for angle in output.angles
            ],
        }
        prompts_path.write_text(json.dumps(prompts_payload, indent=2), encoding="utf-8")

        manifest = CampaignManifest(
            campaign_id=campaign_id,
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat(),
            provider=provider,
            mode=mode,
            brief=brief,
            output=output,
            artifacts=SavedArtifact(
                manifest_path=str(manifest_path.relative_to(self.repo_root)),
                copy_output_path=str(copy_path.relative_to(self.repo_root)),
                brief_path=str(brief_path.relative_to(self.repo_root)),
                prompts_path=str(prompts_path.relative_to(self.repo_root)),
            ),
        )
        manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return manifest

    def load(self, campaign_id: str) -> CampaignManifest | None:
        manifest_path = self.manifest_dir / f"{campaign_id}.json"
        if not manifest_path.exists():
            return None
        return CampaignManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))

    def list_campaigns(self) -> list[CampaignManifest]:
        manifests = sorted(self.manifest_dir.glob("*.json"), reverse=True)
        return [
            CampaignManifest.model_validate_json(path.read_text(encoding="utf-8"))
            for path in manifests
        ]

    def campaign_image_dir(self, campaign_id: str) -> Path:
        return self.image_dir / campaign_id

    def image_manifest_path(self, campaign_id: str) -> Path:
        return self.campaign_image_dir(campaign_id) / "manifest.json"

    def save_image_manifest(self, manifest: ImageGenerationManifest) -> ImageGenerationManifest:
        image_dir = self.campaign_image_dir(manifest.campaign_id)
        image_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = self.image_manifest_path(manifest.campaign_id)
        manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return manifest

    def load_image_manifest(self, campaign_id: str) -> ImageGenerationManifest | None:
        manifest_path = self.image_manifest_path(campaign_id)
        if not manifest_path.exists():
            return None
        return ImageGenerationManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))

    def overwrite_campaign(self, manifest: CampaignManifest) -> CampaignManifest:
        copy_path = self.copy_dir / f"{manifest.campaign_id}.json"
        brief_path = self.brief_dir / f"{manifest.campaign_id}.json"
        prompts_path = self.prompt_dir / f"{manifest.campaign_id}.json"
        manifest_path = self.manifest_dir / f"{manifest.campaign_id}.json"
        copy_path.write_text(json.dumps(manifest.output.model_dump(mode="json"), indent=2), encoding="utf-8")
        brief_path.write_text(manifest.brief.model_dump_json(indent=2), encoding="utf-8")
        prompts_payload = {
            "campaign_id": manifest.campaign_id,
            "angles": [
                {
                    "angle_id": angle.angle_id,
                    "title": angle.title,
                    "image_prompts": angle.image_prompts,
                }
                for angle in manifest.output.angles
            ],
        }
        prompts_path.write_text(json.dumps(prompts_payload, indent=2), encoding="utf-8")
        manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return manifest

    def export_zip_path(self, campaign_id: str) -> Path:
        return self.export_dir / f"{campaign_id}.zip"
