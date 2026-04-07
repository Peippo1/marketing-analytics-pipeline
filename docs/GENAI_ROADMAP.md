# GenAI Roadmap

## Phase 1: Brief Copilot

CampaignForge AI now includes a brief copilot layer that can:

- accept a structured campaign brief
- generate a campaign summary
- suggest personas and channels
- create three campaign angles
- produce headline, body copy, and CTA variants
- generate image prompts for a later visual generation stage
- save outputs under `data/generated/`

The current implementation supports:

- `mock` mode for local demos with no external API key
- optional `openai` mode when `OPENAI_API_KEY` and `CAMPAIGNFORGE_LLM_PROVIDER=openai` are set

## Phase 2: Image Generation

CampaignForge AI now also includes:

- provider-swappable image generation
- saved image outputs and metadata under `data/generated/images/<campaign_id>/`
- FastAPI endpoints for image generation and retrieval
- a Streamlit gallery flow for selecting campaigns, prompts, and saved concepts

Current scope:

- mock SVG generation by default for local demos
- optional OpenAI-compatible live image generation when environment variables are configured

Still planned:

- regenerate and approve/reject flows

## Phase 3: Workflow Product Polish

Planned next steps:

- exportable campaign packs
- saved campaign history and retrieval
- reusable industry templates
- tone presets and brand guardrails
- basic auth if hosted
