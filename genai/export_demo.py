from __future__ import annotations

import argparse

from genai.service import CampaignExportService


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a CampaignForge AI campaign bundle.")
    parser.add_argument("--campaign-id", required=True, help="Campaign id to export.")
    args = parser.parse_args()

    export_path = CampaignExportService().export_campaign(args.campaign_id)
    print(f"Exported campaign bundle: {export_path}")


if __name__ == "__main__":
    main()
