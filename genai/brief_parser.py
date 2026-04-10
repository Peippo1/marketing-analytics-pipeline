from __future__ import annotations

from collections import Counter
import re

from genai.schemas import CampaignBrief, PersonaSuggestion


DEFAULT_TONES = ["Confident", "Practical", "Supportive"]


def slugify_campaign_name(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "campaign"


def infer_channel_recommendations(brief: CampaignBrief) -> list[str]:
    explicit = [channel.strip() for channel in brief.channels if channel.strip()]
    if explicit:
        return explicit[:4]

    text = f"{brief.brief} {brief.target_market or ''}".lower()
    signals = {
        "linkedin": "LinkedIn",
        "b2b": "LinkedIn",
        "professional": "LinkedIn",
        "instagram": "Instagram",
        "visual": "Instagram",
        "meta": "Meta Ads",
        "facebook": "Meta Ads",
        "email": "Email",
        "newsletter": "Email",
        "launch": "Landing Page",
        "search": "Search Ads",
    }
    scores = Counter()
    for keyword, channel in signals.items():
        if keyword in text:
            scores[channel] += 1

    ranked = [channel for channel, _ in scores.most_common()]
    if not ranked:
        ranked = ["LinkedIn", "Email", "Landing Page"]
    return ranked[:4]


def infer_tone_options(brief: CampaignBrief) -> list[str]:
    tones = [tone.strip().title() for tone in brief.tones if tone.strip()]
    if tones:
        seen = list(dict.fromkeys(tones))
        return seen[:4]
    return DEFAULT_TONES


def build_campaign_summary(brief: CampaignBrief) -> str:
    product_name = brief.product_name or brief.campaign_name or "the offer"
    target_market = brief.target_market or "the target audience"
    goals = ", ".join(brief.goals[:2]) if brief.goals else "awareness and conversion"
    return (
        f"CampaignForge AI should position {product_name} for {target_market}, "
        f"using a concise campaign story focused on {goals}. The brief should translate "
        "into reusable messaging angles, channel-specific copy, and prompt-ready creative direction."
    )


def build_persona_suggestions(brief: CampaignBrief) -> list[PersonaSuggestion]:
    target = brief.target_market or "growth-oriented teams"
    product_name = brief.product_name or brief.campaign_name or "the product"
    return [
        PersonaSuggestion(
            name="Efficiency-Focused Operator",
            description=f"A practical buyer in {target} looking for faster ways to deliver results.",
            motivations=["Save time", "Reduce workflow friction", f"Adopt tools like {product_name} quickly"],
            pain_points=["Too many manual steps", "Unclear ROI", "Hard-to-reuse campaign process"],
        ),
        PersonaSuggestion(
            name="Performance-Minded Marketer",
            description="A marketing lead who wants measurable uplift without bloated tooling.",
            motivations=["Improve campaign output", "Increase consistency", "Create repeatable assets"],
            pain_points=["Creative inconsistency", "Slow execution", "Fragmented campaign systems"],
        ),
        PersonaSuggestion(
            name="Decision-Maker Sponsor",
            description="A stakeholder evaluating whether the campaign concept feels credible and commercially useful.",
            motivations=["See a polished workflow", "Validate practical value", "Minimize implementation risk"],
            pain_points=["Vague AI promises", "Thin demo experiences", "Lack of exportable outputs"],
        ),
    ]
