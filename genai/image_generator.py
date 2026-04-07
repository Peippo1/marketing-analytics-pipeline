from __future__ import annotations

import base64
from html import escape
import os
from pathlib import Path
from typing import Protocol
from uuid import uuid4

import requests

from genai.schemas import GeneratedImageAsset


class ImageGenerator(Protocol):
    provider_name: str
    mode: str

    def generate(
        self,
        output_dir: Path,
        campaign_id: str,
        prompt: str,
        style: str,
        count: int,
    ) -> list[GeneratedImageAsset]: ...


def _safe_style_token(style: str) -> str:
    token = "".join(char.lower() if char.isalnum() else "-" for char in style).strip("-")
    return token or "concept"


class MockImageGenerator:
    provider_name = "mock"
    mode = "mock"

    def generate(
        self,
        output_dir: Path,
        campaign_id: str,
        prompt: str,
        style: str,
        count: int,
    ) -> list[GeneratedImageAsset]:
        output_dir.mkdir(parents=True, exist_ok=True)
        assets: list[GeneratedImageAsset] = []
        style_token = _safe_style_token(style)
        colors = [
            ("#10233f", "#d8a73e"),
            ("#1f4a73", "#f7c35f"),
            ("#233b2f", "#85c7a6"),
            ("#512f5f", "#f1af8e"),
        ]

        for index in range(count):
            image_id = uuid4().hex[:12]
            filename = f"{campaign_id}-{style_token}-{index + 1}-{image_id}.svg"
            file_path = output_dir / filename
            primary, accent = colors[index % len(colors)]
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="628" viewBox="0 0 1200 628">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{primary}" />
      <stop offset="100%" stop-color="{accent}" />
    </linearGradient>
  </defs>
  <rect width="1200" height="628" fill="url(#bg)" rx="30" />
  <rect x="68" y="64" width="1064" height="500" rx="22" fill="rgba(255,255,255,0.14)" stroke="rgba(255,255,255,0.18)" />
  <text x="94" y="124" font-size="28" font-family="Helvetica, Arial, sans-serif" fill="#f6f3ee" letter-spacing="3">CAMPAIGNFORGE AI</text>
  <text x="94" y="210" font-size="60" font-weight="700" font-family="Helvetica, Arial, sans-serif" fill="#ffffff">{escape(style)}</text>
  <foreignObject x="94" y="252" width="700" height="210">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Helvetica, Arial, sans-serif; color: #f8f5ef; font-size: 28px; line-height: 1.35;">
      {escape(prompt[:220])}
    </div>
  </foreignObject>
  <rect x="94" y="500" width="290" height="44" rx="22" fill="rgba(255,255,255,0.22)" />
  <text x="118" y="529" font-size="24" font-family="Helvetica, Arial, sans-serif" fill="#ffffff">Mock concept {index + 1}</text>
</svg>
"""
            file_path.write_text(svg, encoding="utf-8")
            assets.append(
                GeneratedImageAsset(
                    image_id=image_id,
                    prompt=prompt,
                    style=style,
                    provider=self.provider_name,
                    mode=self.mode,
                    file_path=str(file_path),
                    mime_type="image/svg+xml",
                )
            )
        return assets


class OpenAIImageGenerator:
    provider_name = "openai"
    mode = "live"

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")

    def generate(
        self,
        output_dir: Path,
        campaign_id: str,
        prompt: str,
        style: str,
        count: int,
    ) -> list[GeneratedImageAsset]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        output_dir.mkdir(parents=True, exist_ok=True)
        response = requests.post(
            f"{self.base_url}/images/generations",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "prompt": f"{prompt}\nStyle direction: {style}",
                "size": "1024x1024",
                "n": count,
                "response_format": "b64_json",
            },
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
        assets: list[GeneratedImageAsset] = []
        style_token = _safe_style_token(style)

        for index, item in enumerate(payload.get("data", []), start=1):
            image_id = uuid4().hex[:12]
            filename = f"{campaign_id}-{style_token}-{index}-{image_id}.png"
            file_path = output_dir / filename
            file_path.write_bytes(base64.b64decode(item["b64_json"]))
            assets.append(
                GeneratedImageAsset(
                    image_id=image_id,
                    prompt=prompt,
                    style=style,
                    provider=self.provider_name,
                    mode=self.mode,
                    file_path=str(file_path),
                    mime_type="image/png",
                )
            )
        return assets


def get_image_generator() -> ImageGenerator:
    provider = os.getenv("CAMPAIGNFORGE_IMAGE_PROVIDER", "mock").lower()
    if provider == "openai":
        return OpenAIImageGenerator()
    return MockImageGenerator()
