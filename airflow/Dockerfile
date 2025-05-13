FROM apache/airflow:2.9.1-python3.10

COPY requirements-airflow.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt && rm /requirements.txt