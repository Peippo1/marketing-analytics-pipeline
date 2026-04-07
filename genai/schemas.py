from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class CampaignBrief(BaseModel):
    campaign_name: Optional[str] = Field(default=None, max_length=120)
    brief: str = Field(min_length=20, max_length=4000)
    product_name: Optional[str] = Field(default=None, max_length=120)
    target_market: Optional[str] = Field(default=None, max_length=240)
    goals: List[str] = Field(default_factory=list)
    channels: List[str] = Field(default_factory=list)
    tones: List[str] = Field(default_factory=list)
    brand_keywords: List[str] = Field(default_factory=list)
    banned_words: List[str] = Field(default_factory=list)
    compliance_notes: List[str] = Field(default_factory=list)


class PersonaSuggestion(BaseModel):
    name: str
    description: str
    motivations: List[str]
    pain_points: List[str]


class CampaignAngle(BaseModel):
    angle_id: str
    title: str
    summary: str
    tone: str
    recommended_channels: List[str]
    headlines: List[str]
    body_copy: List[str]
    ctas: List[str]
    image_prompts: List[str]


class CampaignOutput(BaseModel):
    campaign_summary: str
    audience_suggestions: List[PersonaSuggestion]
    channel_recommendations: List[str]
    tone_options: List[str]
    angles: List[CampaignAngle]


class SavedArtifact(BaseModel):
    manifest_path: str
    copy_output_path: str


class CampaignManifest(BaseModel):
    campaign_id: str
    created_at: str
    provider: str
    mode: str
    brief: CampaignBrief
    output: CampaignOutput
    artifacts: SavedArtifact

