

"""
DAG: Model Evaluation
Description: Runs the evaluate_model.py script to evaluate the trained model and saves metrics.
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    dag_id='model_evaluation_dag',
    default_args=default_args,
    description='Evaluate trained model and save metrics',
    schedule_interval=None,  # Trigger manually or set a cron schedule
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['model', 'evaluation'],
) as dag:

    evaluate_model = BashOperator(
        task_id='evaluate_model',
        bash_command='python3 /opt/models/evaluate_model.py',
    )

    evaluate_model