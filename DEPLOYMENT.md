# Deployment Guide

## Local Setup

Recommended path:

```bash
make setup
```

This creates a local Python environment and installs development dependencies.

If you prefer manual installation:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -r requirements-airflow.txt
pip install -r requirements-streamlit.txt
```

## Fast Demo Path

For a quick under-5-minute demo:

```bash
make demo
```

This runs:

- local setup automatically if `.venv` is missing
- ETL
- model training
- model evaluation

Demo outputs are collected under:

```text
demo_outputs/latest/
```

## Local App Runs

Run the API:

```bash
make api
```

Run the Streamlit dashboard:

```bash
make dashboard
```

## Docker

Build the Streamlit image:

```bash
docker build -t marketing-analytics-app .
```

Run the Streamlit container:

```bash
docker run -p 8501:8501 marketing-analytics-app
```

Build the FastAPI image:

```bash
docker build -t fastapi-app:latest -f Dockerfile.fastapi .
```

Run the FastAPI container:

```bash
docker run -p 8000:8000 fastapi-app:latest
```

## Airflow

Start the Airflow environment:

```bash
cd airflow
docker compose up --build
```

## Configuration Notes

- Local secrets should be provided through `.env`
- Streamlit secrets should be provided through `.streamlit/secrets.toml`
- Start from `.env.example` for environment variables where applicable
- CRM and Google Sheets integrations require valid credentials before live use

## Intended Deployment Use

This repository includes deployment assets for:

- local demo and review
- Docker-based packaging
- Kubernetes discussion or extension
- Airflow-based orchestration examples

It is best treated as a starter codebase or downloadable asset, not as a production-managed deployment template without further project-specific hardening.
