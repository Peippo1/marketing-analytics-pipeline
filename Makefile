PYTHON ?= python

.PHONY: setup test train evaluate api dashboard airflow

setup:
	./setup.sh

test:
	$(PYTHON) -m pytest tests/

train:
	$(PYTHON) models/train_model.py

evaluate:
	$(PYTHON) models/evaluate_model.py

api:
	uvicorn scoring.fastapi_app:app --reload

dashboard:
	streamlit run streamlit_app.py

airflow:
	cd airflow && docker compose up --build
