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
    etl_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts/prepare_data.py'))
    result = subprocess.run(
        ['python', etl_script_path],
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