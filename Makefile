PYTHON ?= python

.PHONY: setup demo genai-demo genai-image-demo test train evaluate api dashboard run-dashboard airflow

setup:
	./setup.sh

demo:
	./run-demo.sh

genai-demo:
	$(PYTHON) -m genai.demo

genai-image-demo:
	$(PYTHON) -m genai.image_demo --campaign-id $$(ls -1t data/generated/manifests/*.json | head -n 1 | xargs basename | sed 's/\.json$$//')

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
