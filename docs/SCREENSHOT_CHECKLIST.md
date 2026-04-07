# Screenshot Checklist

Use this checklist when preparing a marketplace listing, portfolio post, or buyer handoff deck.

## README / Repository

- Repository landing page with project title and badges visible
- README top section showing the value proposition
- Architecture diagram section

## Terminal / Execution

- `make setup` success output
- ETL run output
- `make train` output with successful completion
- `make evaluate` output with metrics visible

## API

- FastAPI `/health` response
- FastAPI `/customers` response
- Optional `/docs` page if enabled locally for demo purposes

## Dashboard

- Full dashboard landing screen with hero section visible
- Metric cards row
- Dataset preview section
- CRM sync panel in dry-run mode
- Dry-run result message after action

## Ops / Delivery

- GitHub Actions checks screen
- Docker build commands or output
- `airflow/` and `k8s/` directory view for deployment credibility

## Capture Tips

- Prefer desktop-width screenshots for the dashboard
- Keep terminal output clean by using a fresh shell session
- Use dry-run modes for integrations so screens remain safe to share
- Avoid including local usernames, tokens, or machine-specific paths
