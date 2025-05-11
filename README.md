# 📊 Marketing Analytics Pipeline
A modular ETL and Machine Learning pipeline for marketing analytics, built with Pandas, scikit-learn, MLflow, and orchestrated with Airflow.

This project demonstrates a full end-to-end data engineering and ML workflow for a marketing analytics use case, including ETL, feature engineering, model training, and dashboarding.

## 🚀 Project Goals

- Build a scalable ETL pipeline to clean and enrich marketing data
- Perform feature engineering for predictive modeling
- Train and evaluate machine learning models for lead scoring
- Schedule ETL and model training pipelines with Airflow
- Visualize insights interactively using Streamlit

## 🧱 Tech Stack

- **Language**: Python
- **Data Processing**: Pandas
- **ML/AI**: scikit-learn, MLflow
- **Scheduling**: Airflow (Docker Compose)
- **Dashboarding**: Streamlit
- **Database**: MySQL (optional, not required for core pipeline)
- **Data Source**: [Kaggle Marketing Data](https://www.kaggle.com/datasets/jackdaoud/marketing-data)

## 📁 Project Structure

```
marketing-analytics-pipeline/
├── data/
│   ├── raw/               # Raw zipped marketing data
│   └── processed/         # Cleaned processed CSVs
├── etl/
│   └── marketing_etl.py   # ETL: unzip, clean, feature engineer, save processed data
├── models/
│   ├── artifacts/          # Saved trained models (timestamped .pkl)
│   ├── versioning.py        # Model versioning utilities
│   ├── run_mlflow_flask.py  # Local MLflow server launcher (Waitress)
│   ├── train_model.py     # Model training script
│   ├── evaluate_model.py  # Model evaluation script
│   ├── model.py           # Model utilities
│   └── model_config.yaml  # Model config file
├── airflow/
│   ├── dags/
│   │   ├── marketing_etl_dag.py
│   │   ├── model_training_dag.py
│   │   └── model_evaluation_dag.py
│   ├── scripts/
│   │   ├── prepare_data.py
│   │   └── convert_delta_to_csv.py
│   └── docker-compose.yaml
├── dashboard/
│   └── streamlit_app.py    # Streamlit dashboard with model metrics and CRM sync
├── requirements.txt
└── README.md
```

## ▶️ Running the Pipeline Locally

### 1. Set up the Environment

```bash
pip install -r requirements.txt
```

### 2. Run the ETL Process

```bash
python etl/marketing_etl.py
```

This will load the raw data from either a CSV (`ifood_df.csv`) or a ZIP file (`ifood_data.zip`), clean and enrich it, and save the processed data to `data/processed/processed_marketing_data.csv`.

### 3. Train the Model

```bash
python models/train_model.py
```

This will train a logistic regression model based on configuration in `models/model_config.yaml` and save the model artifact in `models/`.

### 3.5. Launch MLflow Tracking Server

```bash
python run_mlflow_flask.py 5001
```
This launches a local MLflow UI to track experiments and models at `http://localhost:5001`.

Make sure to keep this terminal open while training models!

### 4. Evaluate the Model

```bash
python models/evaluate_model.py
```

This will load the trained model and processed dataset, evaluate model performance (accuracy, precision, recall, F1 score), and print the results.

Evaluation metrics are now also logged automatically into MLflow for experiment tracking.

### 5. Visualize with Streamlit (Optional)

```bash
streamlit run dashboard/streamlit_app.py
```

Launches the interactive dashboard to view model versions, metrics, and score customer files. Includes Google Sheets sync functionality.

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

Includes basic feature engineering: creation of customer age, tenure, and aggregated spend categories.

**Note:** The project now supports clean environment setup via the `setup.sh` script.

## ⚙️ Environment Setup (New)

To simplify setup on a new machine, this project includes a `setup.sh` script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Ensure Python 3.11.9 is available (via pyenv)
- Create a virtual environment
- Install all project dependencies from `requirements.txt`
- Warn you if the `.streamlit/secrets.toml` file is missing (needed for Google Sheets integration)

## 🧩 Google Sheets CRM Integration

You can sync scored customer data directly to a Google Sheet from the dashboard.

### 🔑 Setup Instructions

1. Create a Google Cloud service account with Sheets API access
2. Convert the key JSON to TOML format and save it to:
```
.streamlit/secrets.toml
```
(You can use Streamlit's secrets management with `.streamlit/secrets.toml`)
3. Share the target Google Sheet with the service account email
4. Use the "Sync to Google Sheets" button in the dashboard to send scored data

The default sheet is named **Scored_Customers**.

## 🔜 Next Steps

- [x] Complete ETL pipeline and convert to reusable scripts
- [x] Run exploratory analysis on customer behavior
- [x] Build segmentation or response model
- [x] Deploy dashboard for insights
- [x] Add unit tests for pipeline components
- [x] Containerize with Docker for local + cloud execution
- [x] Schedule daily pipeline using Airflow (via docker-compose + DAG)
- [x] Expand ETL script for dynamic raw data handling and basic feature engineering
- [x] Automate model training pipeline
- [ ] Add support for CRM push via Salesforce/HubSpot APIs

## 🛠️ Future Improvements

- Add CI/CD pipeline for automatic deployment
- Migrate to full PySpark processing
- Incorporate model monitoring with MLflow
- Expand customer segmentation modeling
- Integrate model deployment pipeline via MLflow Registry
- Integrate webhook/CRM actions after model scoring

## ⏰ Airflow DAG Scheduling

This project includes Airflow DAGs to run the ETL and model training pipelines on a scheduled basis.

### DAGs

- `marketing_etl_dag.py`: Runs the ETL process.
- `model_training_dag.py`: Runs model training using the processed dataset.
- `model_evaluation_dag.py`: Runs model evaluation on the trained model.

- Located in the `airflow/dags/` directory.
- Runs the full ETL and model training processes using Pandas scripts.
- Output is written as CSV files to the `data/processed/` directory.
- Scripts used in the DAG are located in `airflow/scripts/`

### Run with Docker Compose

From the `airflow/` directory, start Airflow using:

```bash
docker compose up
```

Then visit the Airflow UI at [http://localhost:8080](http://localhost:8080).

Ensure the DAGs are switched 'on' and manually trigger runs for testing.
- You can also inspect the logs or run tasks manually using the CLI: `docker compose exec airflow-webserver airflow tasks list marketing_etl_dag`

### Notes

- Logs are available in the Airflow UI per task run.
- If using multiple Airflow components, ensure all share the same `secret_key` under the `[webserver]` section of `airflow.cfg`.

## ♻️ Housekeeping

- Removed all `__pycache__/` directories to keep repo clean
- `.gitignore` updated to exclude `__pycache__/` and `.DS_Store` files
