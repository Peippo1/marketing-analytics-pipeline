from __future__ import annotations

import argparse

from genai.schemas import ImageGenerationRequest
from genai.service import CampaignImageService


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CampaignForge AI image generation demo.")
    parser.add_argument("--campaign-id", required=True, help="Campaign manifest id to use for image generation.")
    parser.add_argument("--style", default="Campaign concept board", help="Style direction for the generated concepts.")
    parser.add_argument("--count", type=int, default=2, help="Number of concepts to generate.")
    args = parser.parse_args()

    manifest = CampaignImageService().generate_and_save(
        ImageGenerationRequest(
            campaign_id=args.campaign_id,
            style=args.style,
            count=args.count,
        )
    )
    print(f"Generated image concepts for: {manifest.campaign_id}")
    print(f"Saved {len(manifest.assets)} assets in data/generated/images/{manifest.campaign_id}/")


if __name__ == "__main__":
    main()
