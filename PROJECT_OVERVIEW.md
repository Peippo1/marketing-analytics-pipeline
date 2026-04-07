# CampaignForge AI Overview

## Summary

`CampaignForge AI` is a portfolio-ready marketing intelligence application that demonstrates an end-to-end workflow for campaign and customer data operations. It combines ETL, feature engineering, model training, a GenAI brief copilot, optional image concept generation, API delivery, dashboard presentation, and workflow orchestration in one repository.

## What A Buyer Gets

- A Python marketing workflow codebase covering ingestion, transformation, modeling, and presentation
- A GenAI layer that turns campaign briefs into structured copy outputs and concept-image prompts
- A FastAPI service for exposing customer-facing or internal scoring endpoints
- A Streamlit dashboard for stakeholder-friendly reporting and CRM workflow demos
- Airflow DAGs, Dockerfiles, and Kubernetes manifests to support deployment conversations
- GitHub Actions workflows and automated tests for baseline engineering hygiene

## Core Capabilities

- ETL pipeline for cleaning and enriching campaign and customer datasets
- Scikit-learn training flow for lead-scoring style classification
- Model evaluation and artifact generation
- Optional image concept generation with mock-first local mode
- CRM export examples for Salesforce and HubSpot
- Google Sheets synchronization example for lightweight ops workflows
- Optional OpenTelemetry instrumentation for the FastAPI service

## Commercial Positioning

This repository is best positioned as:

- a portfolio-quality campaign intelligence engineering sample
- a starter codebase for internal marketing analytics tools
- a demo project for buyers wanting Python, FastAPI, Streamlit, and Airflow in one package

It is not positioned as a finished SaaS product. Its value is in demonstrating architecture, implementation quality, deployment readiness, and integration patterns.

## Recommended Demo Story

1. Show the project structure and explain the end-to-end architecture.
2. Run the one-command demo with `make demo`.
3. Review `demo_outputs/latest/` to show the saved outputs.
4. Launch the API with `make api` and show `/health` plus `/customers`.
5. Launch the dashboard with `make dashboard` and walk through scoring and CRM export flows.
6. Highlight Docker, Kubernetes, and Airflow assets as operational maturity indicators.

## Suggested Buyer Talking Points

- Clear separation between app, pipeline, orchestration, and deployment concerns
- Security-conscious defaults and reduced dependency risk
- Test coverage and CI workflows already in place
- Lightweight enough for handoff, extension, or white-label adaptation
- Easy to demonstrate visually thanks to the dashboard and API entry points

## Contents To Highlight In A Listing

- `README.md` for quick-start and architecture
- `Makefile` for demo commands
- `scoring/fastapi_app.py` for API delivery
- `streamlit_app.py` for dashboard UX
- `airflow/dags/` for orchestration examples
- `k8s/` and Dockerfiles for deployment readiness
