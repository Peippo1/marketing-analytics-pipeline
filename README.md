[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dependency graph](https://img.shields.io/github/dependencies-analyzability/Peippo1/marketing-analytics-pipeline?label=dependency%20graph)](https://github.com/Peippo1/marketing-analytics-pipeline/network/dependencies)

# Marketing Analytics Pipeline
A sale-ready developer asset for demonstrating a complete marketing analytics workflow: ingest data, transform it, train a lead-scoring model, evaluate outputs, expose an API, and present results in a dashboard.

This repository is positioned as a reusable code asset for buyers who want a credible analytics starter project, internal demo platform, or portfolio-grade Python data application. It is not marketed as a finished SaaS product.

## What It Does

- Processes raw marketing data into cleaned, analysis-ready datasets
- Trains and evaluates a scikit-learn classification model for lead-scoring style use cases
- Exposes lightweight customer endpoints through FastAPI
- Presents customer data and CRM handoff workflows through Streamlit
- Includes Airflow, Docker, and Kubernetes assets to support deployment and operations discussions

## Who It's For

- Buyers looking for a full-stack Python analytics demo they can adapt or white-label
- Agencies or freelancers who need a credible starter codebase for internal analytics tooling
- Founders or teams who want a presentable example of ETL, modeling, API delivery, and dashboard UX in one repo
- Portfolio buyers who value engineering breadth, deployment readiness, and documented workflows

## What’s Included

- Source-first repository with generated outputs removed from version control
- ETL scripts, model training, and model evaluation workflow
- FastAPI service and Streamlit dashboard
- CRM integration examples for Salesforce and HubSpot
- Google Sheets sync example
- GitHub Actions workflows and automated tests
- Dockerfiles, Kubernetes manifests, and Airflow DAGs
- Supporting sale/demo docs:
  - `PROJECT_OVERVIEW.md`
  - `docs/DEMO_SCRIPT.md`
  - `docs/SCREENSHOT_CHECKLIST.md`
  - `docs/SAMPLE_OUTPUTS.md`

## Quickstart

The fastest local setup path is:

```bash
make demo
```

What those commands do:

- `make demo`: bootstraps the local environment if needed, then runs ETL, model training, and evaluation end-to-end using the included sample dataset

The bundled demo input is already included under `data/raw/`.

After `make demo`, the most useful outputs are gathered in:

```text
demo_outputs/latest/
```

That folder contains:

- the latest trained model artifact
- the training metrics JSON
- the evaluation metrics JSON
- a small readme for quick inspection

If you want to continue the full interactive walkthrough after the demo run:

```bash
make api
make dashboard
```

If you prefer to prepare the environment explicitly first, you can still run:

```bash
make setup
make demo
```

If you prefer manual setup:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-airflow.txt
pip install -r requirements-streamlit.txt
```

## Demo

Recommended buyer demo flow:

1. Run `make demo`
2. Open `demo_outputs/latest/` and review the generated outputs
3. Launch the API with `make api`
4. Launch the dashboard with `make dashboard`

Useful companion docs:

- `PROJECT_OVERVIEW.md` for a buyer-facing summary
- `docs/DEMO_SCRIPT.md` for a guided walkthrough
- `docs/SCREENSHOT_CHECKLIST.md` for listing or portfolio prep
- `docs/SAMPLE_OUTPUTS.md` for reusable output snippets
- `docs/LISTING_COPY.md` for repo description and marketplace copy
- `docs/ASSET_PREP.md` for screenshots, GIFs, and listing asset planning

## Project Structure

```text
marketing-analytics-pipeline/
├── airflow/                  # Airflow DAGs, scripts, and container setup
├── data/raw/                 # Sample raw dataset and supporting assets
├── docs/                     # Demo, screenshot, and sales-support material
├── etl/                      # ETL pipeline scripts
├── k8s/                      # Kubernetes deployment manifests
├── models/                   # Training, evaluation, and artifact-related code
├── pipelines/                # Pipeline helper modules
├── scoring/                  # FastAPI application
├── tests/                    # Automated tests
├── utils/                    # CRM and Google Sheets helpers
├── streamlit_app.py          # Canonical Streamlit dashboard entrypoint
├── Makefile                  # Common developer/demo commands
├── setup.sh                  # Local setup helper
└── README.md
```

## Tech Stack

| Area | Tools |
| --- | --- |
| Language | Python 3.11 |
| Data processing | Pandas |
| ML | scikit-learn |
| API | FastAPI |
| Dashboard | Streamlit |
| Scheduling | Apache Airflow |
| Packaging | Docker |
| Deployment assets | Kubernetes manifests |
| Observability | OpenTelemetry hooks for FastAPI |
| Integrations | Salesforce, HubSpot, Google Sheets |

## Why This Is Useful

- Shows an end-to-end analytics workflow in one reviewable repository
- Gives buyers a realistic starting point rather than isolated notebooks or toy scripts
- Demonstrates breadth across ETL, model training, API delivery, dashboard UX, and orchestration
- Provides a stronger portfolio or resale asset than a single-purpose machine learning script
- Includes deployment and CI assets that help the project feel operationally credible

## Comparison

| Capability | Included |
| --- | --- |
| Source code | Yes |
| Local run path | Yes |
| One-command demo | Yes |
| Docker support | Yes |
| Dashboard | Yes |
| API | Yes |
| Tests | Yes |
| Airflow orchestration | Yes |
| Kubernetes manifests | Yes |

## Notes

- The repository currently targets Python `3.11.11` via `.python-version`.
- Generated outputs such as model artifacts, processed data, and local runtime files are intentionally gitignored.
- Demo outputs are collected under `demo_outputs/latest/` for predictable review.
- `streamlit_app.py` is the single supported dashboard entrypoint for demos and local runs.
- Local secrets should be supplied through `.env` and `.streamlit/secrets.toml`; start from `.env.example` where applicable.
- The public GitHub repository description should match this README positioning for consistency.
- Sales assets can be organized under `docs/assets/` without changing the source layout.
