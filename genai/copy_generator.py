from __future__ import annotations

import json
import os
from typing import Protocol

import requests

from genai.brief_parser import build_campaign_summary, build_persona_suggestions, infer_channel_recommendations, infer_tone_options
from genai.prompt_builder import build_image_prompts
from genai.schemas import CampaignAngle, CampaignBrief, CampaignOutput


class CampaignGenerator(Protocol):
    provider_name: str
    mode: str

    def generate(self, brief: CampaignBrief) -> CampaignOutput: ...


class MockCampaignGenerator:
    provider_name = "mock"
    mode = "mock"

    def generate(self, brief: CampaignBrief) -> CampaignOutput:
        channels = infer_channel_recommendations(brief)
        tones = infer_tone_options(brief)
        summary = build_campaign_summary(brief)
        personas = build_persona_suggestions(brief)
        product_name = brief.product_name or brief.campaign_name or "your offer"
        primary_goal = brief.goals[0] if brief.goals else "drive qualified interest"

        angle_templates = [
            (
                "angle-1",
                "Outcome-Driven Launch",
                f"Frame {product_name} as the most direct way to {primary_goal} without adding operational drag.",
            ),
            (
                "angle-2",
                "Credibility Through Process",
                f"Show how {product_name} creates a repeatable campaign workflow that teams can trust and reuse.",
            ),
            (
                "angle-3",
                "Speed With Confidence",
                f"Emphasize faster campaign execution for {brief.target_market or 'modern marketing teams'} while maintaining quality.",
            ),
        ]

        angles = []
        for idx, (angle_id, title, angle_summary) in enumerate(angle_templates):
            tone = tones[idx % len(tones)]
            angle_channels = channels[:2] if idx < 2 else channels[1:3] or channels[:2]
            headlines = [
                f"{product_name} helps teams move from brief to launch faster",
                f"Turn campaign planning into a repeatable growth workflow",
                f"Build credible campaign momentum without extra complexity",
                f"Give your team a clearer path from strategy to execution",
                f"Create campaign-ready outputs with less manual back-and-forth",
            ]
            body_copy = [
                f"{product_name} gives teams a structured way to translate campaign ideas into reusable messaging and campaign assets, making it easier to {primary_goal}.",
                f"Instead of juggling disconnected tools, teams can use {product_name} to align strategy, messaging, and delivery in one practical workflow.",
                f"For teams that need polished outputs quickly, {product_name} offers a more operational path from campaign brief to launch-ready material.",
            ]
            ctas = [
                "Review the campaign plan",
                "Generate the next campaign pack",
                "Start the guided demo",
            ]
            angles.append(
                CampaignAngle(
                    angle_id=angle_id,
                    title=title,
                    summary=angle_summary,
                    tone=tone,
                    recommended_channels=angle_channels,
                    headlines=headlines,
                    body_copy=body_copy,
                    ctas=ctas,
                    image_prompts=build_image_prompts(brief, title, angle_summary, tone, angle_channels),
                )
            )

        return CampaignOutput(
            campaign_summary=summary,
            audience_suggestions=personas,
            channel_recommendations=channels,
            tone_options=tones,
            angles=angles,
        )


class OpenAICampaignGenerator:
    provider_name = "openai"
    mode = "live"

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, brief: CampaignBrief) -> CampaignOutput:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        mock_generator = MockCampaignGenerator()
        schema_hint = mock_generator.generate(brief).model_dump(mode="json")
        prompt = (
            "You are generating campaign planning outputs for a developer product demo. "
            "Return strict JSON matching the provided example keys and list shapes. "
            "Keep all claims realistic, avoid fake metrics, and do not mention unsupported capabilities.\n\n"
            f"Campaign brief:\n{brief.model_dump_json(indent=2)}\n\n"
            f"Example output schema:\n{json.dumps(schema_hint, indent=2)}"
        )
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "temperature": 0.7,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": "Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        return CampaignOutput.model_validate_json(content)


def get_campaign_generator() -> CampaignGenerator:
    provider = os.getenv("CAMPAIGNFORGE_LLM_PROVIDER", "mock").lower()
    if provider == "openai":
        return OpenAICampaignGenerator()
    return MockCampaignGenerator()

