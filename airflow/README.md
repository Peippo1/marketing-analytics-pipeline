# Airflow ETL Scheduler

This module sets up Apache Airflow to orchestrate scheduled ETL tasks for the Marketing Analytics Pipeline. It includes a sample DAG, a Docker Compose setup, and local configuration guidelines.

## Structure

```
airflow/
├── dags/
│   ├── marketing_etl_dag.py   # DAG for scheduled ETL tasks (data extraction, transformation, and loading)
│   ├── train_model_dag.py     # DAG for scheduled model training on processed marketing datasets
│   └── model_evaluation_dag.py # DAG for scheduled model evaluation on the processed marketing dataset
├── docker-compose.yml         # Docker Compose setup for Airflow
├── README.md                  # You're here!
```

## Running Airflow

1. Navigate into the airflow directory:
   ```bash
   cd airflow
   ```

2. (Optional) If not using Docker, install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Airflow using Docker Compose (rebuild with latest changes):
   ```bash
   docker-compose up --build -d
   ```

4. Access the Airflow web interface:
   ```
   http://localhost:8081
   ```

   - Username: `airflow`
   - Password: `airflow`

5. Stop services:
   ```bash
   docker-compose down
   ```

## Notes

- Ensure Docker is running before launching Airflow.
- DAGs must be stored inside the `dags/` directory to be recognized by Airflow.
- `marketing_etl_dag.py` handles extraction, transformation, and loading (ETL) of marketing data.
- `train_model_dag.py` triggers model training on processed marketing datasets.
- `model_evaluation_dag.py` schedules evaluation of the trained model on the processed marketing dataset.
- A `.env` file is supported for local environment variables (e.g., credentials).
- We've locked and patched specific Python dependencies to avoid compatibility issues with `proto`, `google-cloud` libraries, and Airflow provider hooks.
- If you encounter import errors or warnings, double-check `requirements.txt` and ensure the image is rebuilt using:
  ```bash
  docker-compose down --volumes
  docker-compose build --no-cache
  docker-compose up -d
  ```

## Development Notes

- DAGs must be located in `./airflow/dags/` to be recognized by the container.
- Ensure your DAG scripts refer to the correct mounted paths:
  - Use `/opt/airflow/dags/...` for DAG-level scripts.
  - Use `/opt/models/...` for ML-related model training/evaluation scripts.
- If DAGs do not appear in the UI:
  - Ensure the `docker-compose.yml` uses the correct volume path: `./dags:/opt/airflow/dags`
  - Run `docker-compose down --volumes && docker-compose up --build -d` to force volume remount and container rebuild.

## Project Dependencies Displaying in App

If you see unexpected dependency output like:

```
distlib==0.3.9
filelock==3.18.0
...
```

This can happen when the Streamlit app displays standard output from the Docker or Python environment. To suppress it:

- Ensure no `pip freeze` or `!pip install` commands are accidentally being echoed to the UI.
- Review your Streamlit file (`streamlit_app.py`) and remove any debug print or logging that outputs `sys.modules` or similar package data.
- You can redirect unwanted output in Docker by adjusting the entrypoint or using `>/dev/null` for suppressing noise.
