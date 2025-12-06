# 📊 Marketing Analytics Pipeline


[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=Peippo1/marketing-analytics-pipeline)](https://dependabot.com)
[![Dependency graph](https://img.shields.io/github/dependencies-analyzability/Peippo1/marketing-analytics-pipeline?label=dependency%20graph)](https://github.com/Peippo1/marketing-analytics-pipeline/network/dependencies)

## 🏗️ Architecture Diagram

```mermaid
flowchart TD
    A[Marketing Data Source] -->|Raw Data| B[ETL Pipeline (Pandas)]
    B --> C[Feature Engineering]
    C --> D[Model Training & Evaluation (scikit-learn, MLflow)]
    D --> E[Model Artifacts Stored]
    B --> F[Processed Data]
    E --> G[Streamlit Dashboard]
    F --> G
    G --> H[Google Sheets CRM Sync]
    D --> I[FastAPI Service]
    subgraph Kubernetes Cluster
        G
        I
        J[NGINX Ingress Controller]
    end
    J -->|Route traffic| G
    J -->|Route traffic| I
```


# 📊 Marketing Analytics Pipeline
A modular ETL and Machine Learning pipeline for marketing analytics, built with Pandas, scikit-learn, MLflow, and orchestrated with Airflow.

> 📁 Note: Dependencies are split for cleaner environments:
> - `requirements.txt` → shared, security-reviewed pins used by CI
> - `requirements-fastapi.txt` / `requirements-streamlit.txt` → service-specific
> - `airflow/requirements.txt` → extras used inside the Airflow image

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
│   │   ├── train_model_dag.py
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

### 0. 📦 Build and Run with Docker (Airflow)

From the `airflow/` directory, use Docker Compose to run the Airflow environment:

```bash
cd airflow
docker compose down --volumes  # optional: clear volumes
docker compose up --build
```

Then visit the Airflow UI at: [http://localhost:8081](http://localhost:8081)

Ensure the DAGs appear in the UI and are switched ON.

### 1. Set up the Environment

```bash
# For core libraries only:
pip install -r requirements.txt

# For Airflow-specific dependencies:
pip install -r requirements-airflow.txt

# For Streamlit-specific dependencies:
pip install -r requirements-streamlit.txt
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

You can view the dashboard in your browser using one of two methods:

**Option 1: Port Forwarding (Recommended for Local Testing)**
```bash
kubectl port-forward service/streamlit-service 8501:8501
```
Then visit: [http://localhost:8501](http://localhost:8501)

**Option 2: Ingress with Custom DNS**
This project also includes Kubernetes Ingress support to expose the dashboard at a friendly URL:

1. Update `/etc/hosts` with:
   ```
   127.0.0.1 streamlit.local
   ```

2. Apply the ingress:
   ```bash
   kubectl apply -f k8s/ingress.yaml
   ```

3. Access the app via: [http://streamlit.local](http://streamlit.local)

_Note: macOS users may need to flush DNS cache or use a `.test` domain instead of `.local`._

Make sure you have a trained model saved (e.g. `lead_scoring_model_<timestamp>.pkl`) inside the `models/` directory to enable predictions inside the dashboard.

## 🧪 Testing

Unit tests are written using `pytest` and located in the `tests/` directory.

### How to Run Tests

From the project root, run:

```bash
pytest tests/
```

## 🐳 Docker Usage

This project is fully containerized using Docker, supporting both the Streamlit dashboard and the FastAPI service. You can run the entire pipeline and dashboard in reproducible containerized environments, or deploy them on Kubernetes.

Note that Streamlit and Airflow environments are built separately. The Airflow environment uses the `airflow/docker-compose.yml` file to manage the scheduler, webserver, and other components.

### Build the Streamlit Docker Image

```bash
docker build -t marketing-analytics-app .
```

### Run the Streamlit App

```bash
docker run -p 8501:8501 marketing-analytics-app
```

Then open your browser and navigate to `http://localhost:8501`.

Make sure you have a trained model saved (e.g. `lead_scoring_model_<timestamp>.pkl`) inside the `models/` directory to enable predictions inside the container.

You can trigger model training manually using:
```bash
python models/train_model.py
```

## 🐳 FastAPI Docker Usage

To containerize the FastAPI app with the `Dockerfile.fastapi`, follow these steps:
> 🔁 Note: FastAPI app entrypoint has been renamed to `scoring.main:app` to avoid conflicts with the Streamlit dashboard `main.py`.

### Build the FastAPI Docker Image

```bash
docker build -t fastapi-app:latest -f Dockerfile.fastapi .
```

### Run the FastAPI App

```bash
docker run -p 8000:8000 fastapi-app:latest
```

You can access the FastAPI server at `http://localhost:8000`.

## ☸️ Kubernetes Usage

This project now supports Kubernetes deployment to manage the services for Streamlit and FastAPI.

### 1. Set up Minikube and Kubernetes

Start by setting up Minikube and Kubernetes if you haven’t already:

```bash
minikube start
```

Once Minikube is up, you can configure your Kubernetes cluster by running:

```bash
kubectl config use-context minikube
```

### 2. Deploy Services on Kubernetes

After setting up Kubernetes, you can deploy both FastAPI and Streamlit services using the following commands:

#### Deploy FastAPI

```bash
kubectl apply -f k8s/fastapi-deployment.yaml
kubectl apply -f k8s/fastapi-service.yaml
```

#### Deploy Streamlit

```bash
kubectl apply -f k8s/streamlit-deployment.yaml
kubectl apply -f k8s/streamlit-service.yaml
```

### 3. Set up Ingress Controller and Ingress

Set up the NGINX Ingress Controller and Ingress to access the FastAPI and Streamlit services externally:

```bash
kubectl apply -f k8s/ingress.yaml
```

Ensure you have the correct entries in your `/etc/hosts` file to map to the services:

```bash
127.0.0.1   fastapi.local
127.0.0.1   streamlit.local
```

You should now be able to access the services at:

- **FastAPI**: `http://fastapi.local`
- **Streamlit**: `http://streamlit.local`

## 📡 FastAPI Customer Data API

This project includes a FastAPI service that exposes customer data from MySQL.

### ▶️ Running the API Server

```bash
uvicorn scoring.main:app --reload
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
- Installs base dependencies only; Airflow and Streamlit now have their own environment files:
  - `requirements-airflow.txt`
  - `requirements-streamlit.txt`

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

## 🔗 CRM Push (Salesforce / HubSpot)

The Streamlit dashboard now supports pushing the top customers into Salesforce or HubSpot directly.

### Setup

- Salesforce: set `SALESFORCE_INSTANCE_URL` (e.g., `https://your-domain.my.salesforce.com`) and `SALESFORCE_ACCESS_TOKEN`. Optionally set `SALESFORCE_API_VERSION` (defaults to `v60.0`).
- HubSpot: set `HUBSPOT_ACCESS_TOKEN`.

### Usage

1. Load the dashboard and ensure customer data is visible.
2. Pick your CRM in the **CRM Sync** section.
3. Leave **Dry run** checked to preview the payload without sending, or uncheck to push live.
4. Click **Push 20 customers to CRM**.

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
- [x] Deploy Streamlit to Kubernetes with working port-forwarding and Ingress setup
- [x] Add support for CRM push via Salesforce/HubSpot APIs

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
- `train_model_dag.py`: Runs model training using the processed dataset.
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
- for CI-CD testing
