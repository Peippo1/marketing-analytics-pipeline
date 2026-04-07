FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

RUN groupadd --system appuser \
    && useradd --system --gid appuser --create-home --home-dir /home/appuser appuser

COPY requirements-streamlit.txt ./requirements-streamlit.txt
RUN pip install --upgrade pip \
    && pip install -r requirements-streamlit.txt

COPY airflow ./airflow
COPY streamlit_app.py ./streamlit_app.py
COPY utils ./utils

USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]
