# QA Checklist

Use this checklist before the first public sale or before packaging a new release.

## Install

- `make setup` completes on a clean machine
- local `.venv` is created successfully
- required Python packages install without manual fixes
- `.env.example` is sufficient for a safe local start

## Tests

- `python -m pytest tests/` runs successfully
- FastAPI tests pass
- GenAI workflow tests pass
- no unexpected import errors appear in the active Python version

## Demo

- `make demo` completes from a clean repo checkout
- `demo_outputs/latest/` is created
- `demo_outputs/latest/genai/` contains brief, copy, and export artifacts
- `demo_outputs/latest/genai/images/` contains concept image files and image metadata

## Streamlit

- `make dashboard` launches successfully
- the dashboard hero renders correctly
- the Brief Copilot form generates a saved campaign
- the Campaign History panel lists saved campaigns
- the Image Concepts panel generates mock images
- approve / reject / reset actions update image statuses
- export ZIP can be built and downloaded

## FastAPI

- `make api` launches successfully
- `GET /health` returns `200`
- `GET /customers` returns sample or real data
- `POST /genai/brief` returns a saved campaign manifest
- `POST /genai/images` returns saved image metadata
- `POST /genai/campaigns/{campaign_id}/images/review` updates approval state
- `GET /genai/campaigns/{campaign_id}/export` returns a ZIP file

## Export

- exported ZIP opens cleanly
- ZIP contains `brief.json`
- ZIP contains `copy.json`
- ZIP contains `prompts.json`
- ZIP contains `manifest.json`
- ZIP contains `images/` with generated assets when available

## Release Surface

- README matches the shipped workflow
- product docs do not overclaim unsupported features
- screenshots and GIF reflect the current UI
- no generated runtime clutter is tracked in git
