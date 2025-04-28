from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Default args for the DAG
default_args = {
    'owner': 'tim_finch',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'marketing_etl_dag',
    default_args=default_args,
    description='Scheduled ETL DAG for marketing analytics pipeline',
    schedule_interval='@daily',  # You can change this as needed
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

# Python function to run the ETL script
import os

def run_etl():
    etl_script_path = '/opt/airflow/scripts/marketing_etl.py'
    result = subprocess.run(
        ['python', etl_script_path],
        capture_output=True,
        text=True
    )
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    result.check_returncode()

def train_model():
    model_script_path = '/opt/airflow/scripts/train_model.py'
    result = subprocess.run(
        ['python', model_script_path],
        capture_output=True,
        text=True
    )
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)
    result.check_returncode()

# Define the ETL task
etl_task = PythonOperator(
    task_id='run_marketing_etl',
    python_callable=run_etl,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model_after_etl',
    python_callable=train_model,
    dag=dag,
)

etl_task >> train_model_task