from __future__ import annotations

from genai.schemas import CampaignBrief


def build_image_prompts(
    brief: CampaignBrief,
    angle_title: str,
    angle_summary: str,
    tone: str,
    channels: list[str],
) -> list[str]:
    product_name = brief.product_name or brief.campaign_name or "the product"
    brand_keywords = ", ".join(brief.brand_keywords[:4]) if brief.brand_keywords else "clean layout, modern marketing design"
    primary_channel = channels[0] if channels else "digital campaign"
    compliance_note = brief.compliance_notes[0] if brief.compliance_notes else "avoid exaggerated claims"

    prompts = [
        (
            f"{product_name} campaign concept for {primary_channel}, centered on {angle_title}. "
            f"Tone: {tone}. Visual direction: {brand_keywords}. Message focus: {angle_summary}. "
            f"Include room for headline and CTA. Constraint: {compliance_note}."
        ),
        (
            f"Create a polished ad concept for {product_name} that expresses {angle_title} with a {tone.lower()} tone. "
            f"Design for {primary_channel} placement, with clear hierarchy, strong focal point, and marketing-ready composition. "
            f"Brand cues: {brand_keywords}."
        ),
        (
            f"Generate a campaign visual variant for {product_name}. Emphasize {angle_summary}. "
            f"Audience context: {brief.target_market or 'modern digital buyers'}. "
            f"Style: {tone.lower()}, conversion-oriented, adaptable for {', '.join(channels[:2]) or 'web use'}."
        ),
    ]
    return prompts

