from __future__ import annotations

from datetime import datetime, UTC
import json
from pathlib import Path

from genai.schemas import CampaignManifest, CampaignOutput, SavedArtifact


DEFAULT_GENERATED_ROOT = Path(__file__).resolve().parents[1] / "data" / "generated"


class CampaignStorage:
    def __init__(self, root: Path | None = None):
        self.root = root or DEFAULT_GENERATED_ROOT
        self.copy_dir = self.root / "copy"
        self.image_dir = self.root / "images"
        self.manifest_dir = self.root / "manifests"
        for directory in (self.copy_dir, self.image_dir, self.manifest_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def save(self, campaign_id: str, provider: str, mode: str, brief, output: CampaignOutput) -> CampaignManifest:
        copy_path = self.copy_dir / f"{campaign_id}.json"
        manifest_path = self.manifest_dir / f"{campaign_id}.json"

        payload = output.model_dump(mode="json")
        copy_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        manifest = CampaignManifest(
            campaign_id=campaign_id,
            created_at=datetime.now(UTC).isoformat(),
            provider=provider,
            mode=mode,
            brief=brief,
            output=output,
            artifacts=SavedArtifact(
                manifest_path=str(manifest_path.relative_to(self.root.parent)),
                copy_output_path=str(copy_path.relative_to(self.root.parent)),
            ),
        )
        manifest_path.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
        return manifest

    def load(self, campaign_id: str) -> CampaignManifest | None:
        manifest_path = self.manifest_dir / f"{campaign_id}.json"
        if not manifest_path.exists():
            return None
        return CampaignManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))

