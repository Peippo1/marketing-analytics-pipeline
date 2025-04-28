"""
train_model_dag.py

This DAG schedules and runs the model training pipeline for the marketing analytics project.
It executes the 'train_model.py' script located in the 'models' folder using a BashOperator.
The DAG is configured to run daily and retries once if a failure occurs.

Purpose:
- To automate the training of the machine learning model on the latest processed marketing data.
- To ensure the model stays updated with any new data.

Tasks:
- train_model: Executes the training script to fit and save the model.
"""

# Import necessary Airflow classes and standard libraries
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# Default arguments for the DAG
# Includes retry behavior and ownership settings
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG structure and scheduling
with DAG(
    dag_id="train_model_dag",
    default_args=default_args,
    description="Train ML model on processed marketing data",
    schedule_interval="@daily",  # You can change this (e.g., "@weekly", "0 0 * * *", etc.)
    start_date=datetime(2024, 4, 1),
    catchup=False,
    tags=["model_training"],
) as dag:

    # Task: Run the training script using BashOperator
    train_model = BashOperator(
        task_id="train_model",
        bash_command=f"python {os.path.join(os.getcwd(), 'models/train_model.py')}",
    )

    train_model