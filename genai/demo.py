from __future__ import annotations

import argparse
import json
from pathlib import Path

from genai.schemas import CampaignBrief
from genai.service import CampaignBriefService


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CampaignForge AI brief copilot demo.")
    parser.add_argument(
        "--input",
        default="data/demo/campaign_brief.json",
        help="Path to a JSON campaign brief file.",
    )
    args = parser.parse_args()

    brief_path = Path(args.input)
    brief = CampaignBrief.model_validate(json.loads(brief_path.read_text(encoding="utf-8")))
    manifest = CampaignBriefService().generate_and_save(brief)
    print(f"Generated campaign brief output: {manifest.campaign_id}")
    print(f"Manifest: {manifest.artifacts.manifest_path}")
    print(f"Copy output: {manifest.artifacts.copy_output_path}")


if __name__ == "__main__":
    main()

