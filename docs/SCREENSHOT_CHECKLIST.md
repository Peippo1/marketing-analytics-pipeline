# Screenshot Checklist

Use this checklist when preparing a marketplace listing, portfolio post, or buyer handoff deck.

## README / Repository

- Repository landing page with project title and badges visible
- README top section showing the value proposition
- README workflow section showing `Brief -> Strategy -> Copy -> Image Concepts -> Review -> Export`

## Terminal / Execution

- `make demo` success output
- `demo_outputs/latest/` folder view
- generated export ZIP visible in `demo_outputs/latest/genai/`

## API

- FastAPI `/health` response
- FastAPI `/customers` response
- FastAPI `/genai/brief` response
- FastAPI export endpoint returning a ZIP file
- Optional `/docs` page if enabled locally for demo purposes

## Dashboard

- Full dashboard landing screen with hero section visible
- Brief Copilot output section with angles visible
- Campaign History panel with regeneration and export controls
- Image Concepts section with generated mock visuals visible
- Approved or rejected image status visible
- CRM sync panel in dry-run mode

## Ops / Delivery

- GitHub Actions checks screen
- Docker build commands or output
- `airflow/` and `k8s/` directory view for deployment credibility

## Capture Tips

- Prefer desktop-width screenshots for the dashboard
- Keep terminal output clean by using a fresh shell session
- Use dry-run modes for integrations so screens remain safe to share
- Avoid including local usernames, tokens, or machine-specific paths

## Best Screenshot Moments

1. README hero plus workflow section
2. `make demo` finished successfully with the output folder visible
3. Brief Copilot results with angles and copy variants open
4. Image Concepts gallery with at least one approved asset
5. Campaign History panel with the export control visible
6. FastAPI JSON response for `/genai/brief` or `/health`

## GIF Recommendation

- Capture one short 20-30 second GIF showing:
  - selecting a saved campaign
  - generating image concepts
  - approving one concept
  - building and downloading the export ZIP
