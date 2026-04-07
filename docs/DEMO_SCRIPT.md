# Demo Script

## Goal

Use this script for a short buyer-facing walkthrough of the repository.

## Recommended Flow

### 1. Open with the positioning

Say:

`marketing-analytics-pipeline` is a portfolio-ready analytics demo that combines ETL, model training, evaluation, API delivery, dashboard presentation, and orchestration assets in one repository.

### 2. Show the repository structure

Highlight:

- `etl/` for ingestion and transformation
- `models/` for training and evaluation
- `scoring/` for FastAPI delivery
- `streamlit_app.py` for dashboard UX
- `airflow/` for orchestration
- `k8s/` and Dockerfiles for deployment readiness

### 3. Run the core commands

```bash
make setup
python etl/marketing_etl.py
make train
make evaluate
```

Call out:

- reproducible setup
- model artifact generation
- evaluation output saved automatically

### 4. Show the API layer

```bash
make api
```

Then demonstrate:

- `GET /health`
- `GET /customers`

### 5. Show the dashboard

```bash
make dashboard
```

Focus on:

- hero/dashboard presentation
- sample customer dataset panel
- CRM sync dry-run workflow

### 6. Close with operational maturity

Mention:

- GitHub Actions workflows
- Docker and Kubernetes assets
- Airflow orchestration examples
- source-focused repository cleanup and documentation

## Screenshot Checklist

- top of README
- architecture diagram
- model training output in terminal
- evaluation output in terminal
- FastAPI health endpoint
- dashboard landing view
- CRM dry-run action result

## Suggested Buyer Framing

- good fit for portfolio buyers, agencies, or internal analytics teams
- easy to adapt into a starter internal analytics product
- useful as a showcase of full-stack Python analytics engineering
