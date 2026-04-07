PYTHON ?= python

.PHONY: setup demo genai-demo test train evaluate api dashboard run-dashboard airflow

setup:
	./setup.sh

demo:
	./run-demo.sh

genai-demo:
	$(PYTHON) -m genai.demo

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

run-dashboard:
	streamlit run streamlit_app.py

airflow:
	cd airflow && docker compose up --build
