# Release Notes

## v1.0.0

CampaignForge AI is now packaged as a first-sale-ready downloadable developer product centered on a complete campaign workflow:

- Brief capture with structured marketing inputs
- Strategy generation with summaries, personas, channels, and campaign angles
- Copy generation with headlines, body variants, CTAs, and image prompts
- Optional image concept generation with mock-first local mode and swappable live-provider support
- Review workflow with campaign history, regeneration controls, and image approval states
- Campaign export as a ZIP bundle containing the brief, copy, prompts, manifests, and images

### Delivery Surfaces

- Streamlit dashboard for interactive demos
- FastAPI endpoints for programmatic generation, retrieval, review, and export
- One-command local demo flow via `make demo`

### Packaging Improvements

- sale-oriented README and supporting product docs
- buyer-facing demo, listing, and asset prep materials
- structured generated-output folders under `data/generated/`
- repo cleanup and gitignore hardening for local/runtime artifacts

### Notes

- mock mode remains the default for local demos
- live LLM and image generation require environment-variable configuration
- the repository is positioned as a source-code product, not a hosted SaaS application
