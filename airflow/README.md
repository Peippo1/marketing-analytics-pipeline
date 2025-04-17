# Airflow ETL Scheduler

This module sets up Apache Airflow to orchestrate scheduled ETL tasks for the Marketing Analytics Pipeline. It includes a sample DAG, a Docker Compose setup, and local configuration guidelines.

## Structure

```
airflow/
├── dags/
│   └── marketing_etl_dag.py  # Your DAG for scheduling ETL tasks
├── docker-compose.yml        # Docker Compose setup for Airflow
├── README.md                 # You're here!
```

## Running Airflow

1. Navigate into the airflow directory:
   ```bash
   cd airflow
   ```

2. Start Airflow using Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Access the Airflow web interface:
   ```
   http://localhost:8080
   ```

   - Username: `airflow`
   - Password: `airflow`

4. Stop services:
   ```bash
   docker-compose down
   ```

## Notes

- Make sure Docker is running on your machine.
- DAGs should be placed inside the `dags/` folder.
- You can define your environment variables in an `.env` file if needed.

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
