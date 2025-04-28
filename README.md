# 📊 Marketing Analytics Pipeline
A modular ETL pipeline for marketing data built with PySpark and Delta Lake.

This project demonstrates a full end-to-end data engineering workflow for a marketing analytics use case, powered by PySpark, Delta Lake, and the Databricks platform.

We use customer and campaign data (sourced from Kaggle) to extract insights, perform customer segmentation, and explore predictive modelling—all while showcasing best practices in data transformation and Lakehouse architecture.

## 🚀 Project Goals

- Build a scalable ETL pipeline using PySpark and Delta Lake
- Clean, transform, and enrich marketing data
- Generate key KPIs: campaign response rates, customer value, and segment profiles
- Experiment with machine learning models for lead scoring and segmentation
- Visualise insights using Streamlit or Power BI

## 🧱 Tech Stack

- **Language**: Python
- **Data Processing**: Pandas, Scikit-learn (PySpark/Delta Lake planned for future)
- **ML/AI**: scikit-learn, MLflow
- **Scheduling** (optional): Airflow or Databricks Workflows
- **Dashboarding**: Streamlit / Power BI
- **Database**: MySQL hosted on Railway (with secure access via `.env` or Streamlit secrets)
- **Data Source**: [Kaggle Marketing Data](https://www.kaggle.com/datasets/jackdaoud/marketing-data)

## 📁 Project Structure

```
marketing-analytics-pipeline/
├── api/
│   └── main.py
├── data/
│   ├── raw/               # Raw zipped marketing data
│   └── processed/         # Clean processed CSVs
├── etl/
│   └── marketing_etl.py   # Unzips raw data, cleans, saves processed data
├── models/
│   ├── train_model.py     # Model training script
│   ├── model.py           # Model utilities
│   └── model_config.yaml  # Model config file
├── streamlit_app.py       # Interactive dashboard
├── airflow/
│   ├── dags/
│   │   └── marketing_etl_dag.py
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── mysql_utils.py
│   │   ├── prepare_data.py
│   │   └── convert_delta_to_csv.py
│   ├── docker-compose.yaml
├── .streamlit/
│   └── secrets.toml
├── requirements.txt
└── README.md
```

## 🧠 Model Pipeline Features

- Logistic Regression model with scikit-learn
- Config-driven pipeline using model_config.yaml
- 5-fold cross-validation for performance estimation
- Hyperparameter tuning via GridSearchCV
- Versioned model saving (timestamped .pkl files)
- Evaluation metrics saved to JSON for monitoring
- Fallback model loading for robustness
- Configuration-driven training using `model_config.yaml` for features, targets, hyperparameters, and model output paths
- Configurable ETL and model training processes

## 🖥️ Dashboard Features

- Interactive Streamlit app with sidebar navigation
- Filter data by income, marital status, and response
- View dynamic visualizations and summary stats
- Two-column prediction form for lead scoring
- Download filtered data as CSV
- Automatically loads latest trained model
- View live customer data from MySQL database

## 🔐 Configuration

- Secrets and environment credentials are stored in `.streamlit/secrets.toml` for Streamlit Cloud and a `.env` file for local development (both excluded from Git).
- This file is **not tracked** for security purposes and should be created manually:

  ### Example: .streamlit/secrets.toml

  ```
  [mysql]
  host = "your_host"
  user = "your_user"
  password = "your_password"
  database = "your_database"
  ```

  ### Example: .env

  ```
  MYSQL_USER=your_username
  MYSQL_PASSWORD=your_password
  MYSQL_HOST=your_host
  MYSQL_PORT=your_port
  MYSQL_DATABASE=your_database
  ```

  ### Example: model_config.yaml

  ```yaml
  features:
    - Age
    - Income
    - Marital_Status
    - ...
  target_column: Response
  model_params:
    penalty: l2
    solver: lbfgs
    max_iter: 100
  output_model_path: models/
  ```

- The `models/model_config.yaml` file contains configuration settings for model training, including feature selection, target column, model hyperparameters, and output paths. It ensures consistent, reproducible training runs.

- Ensure `.streamlit/secrets.toml` is listed in `.gitignore`.

## 🧪 Testing

Unit tests are written using `pytest` and located in the `tests/` directory.

### How to Run Tests

From the project root, run:

```bash
pytest tests/
```

## 🐳 Docker Usage

This project is fully containerized using Docker. You can run the entire Streamlit dashboard and pipeline in a reproducible containerized environment.

### Build the Docker Image

```bash
docker build -t marketing-analytics-app .
```

### Run the App

```bash
docker run -p 8501:8501 marketing-analytics-app
```

Then open your browser and navigate to `http://localhost:8501`.

Make sure you have a trained model saved (e.g. `lead_scoring_model_<timestamp>.pkl`) inside the `models/` directory to enable predictions inside the container.

You can trigger model training manually using:
```bash
python models/train_model.py
```

## 📡 FastAPI Customer Data API

This project includes a FastAPI service that exposes customer data from MySQL.

### ▶️ Running the API Server

```bash
uvicorn api.main:app --reload
```

- View API data: [http://localhost:8000/customers](http://localhost:8000/customers)
- Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 🔌 Endpoint

- `GET /customers` – Returns the full `customers_cleaned` table from the MySQL database as JSON.
- Uses the same `.env` credentials for connecting to Railway-hosted MySQL.

## 🔜 Next Steps

- [x] Complete ETL pipeline and convert to reusable scripts
- [x] Run exploratory analysis on customer behavior
- [x] Build segmentation or response model
- [x] Deploy dashboard for insights
- [x] Add unit tests for pipeline components
- [x] Containerize with Docker for local + cloud execution
- [x] Schedule daily pipeline using Airflow (via docker-compose + DAG)
- [x] Build ETL script to process raw marketing data into clean CSV
- [ ] Expand ETL script for dynamic raw data handling
- [ ] Automate model training pipeline

## ⏰ Airflow DAG Scheduling

This project includes an Airflow DAG to run the ETL pipeline on a scheduled basis.

### DAG: `marketing_etl_dag`

- Located in the `airflow/dags/` directory.
- Runs the full ETL process using Spark scripts.
- Output is written as Delta Lake files and optionally CSVs to the `data/processed/` directory.
- Scripts used in the DAG are located in `airflow/scripts/`

### Run with Docker Compose

From the `airflow/` directory, start Airflow using:

```bash
docker compose up
```

Then visit the Airflow UI at [http://localhost:8080](http://localhost:8080).

Ensure the DAG is switched 'on' and manually trigger a run for testing.
- You can also inspect the logs or run tasks manually using the CLI: `docker compose exec airflow-webserver airflow tasks list marketing_etl_dag`

### Notes

- Logs are available in the Airflow UI per task run.
- If using multiple Airflow components, ensure all share the same `secret_key` under the `[webserver]` section of `airflow.cfg`.

## ♻️ Housekeeping

- Removed all `__pycache__/` directories to keep repo clean
- `.gitignore` updated to exclude `__pycache__/` and `.DS_Store` files
