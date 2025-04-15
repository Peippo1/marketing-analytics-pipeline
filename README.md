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
- **Data Processing**: PySpark, Delta Lake
- **ML/AI**: scikit-learn, MLflow
- **Scheduling** (optional): Airflow or Databricks Workflows
- **Dashboarding**: Streamlit / Power BI
- **Data Source**: [Kaggle Marketing Data](https://www.kaggle.com/datasets/jackdaoud/marketing-data)

## 📁 Project Structure

```
marketing-analytics-pipeline/
├── data/
│   ├── raw/              # Raw CSVs from Kaggle
│   └── processed/        # Delta output
├── notebooks/
│   └── 01_eda.ipynb      # Exploratory Data Analysis with visual insights
├── pipelines/
│   ├── extract.py        # Load CSV into Spark
│   ├── transform.py      # Clean and engineer features
│   └── load.py           # Save to Delta Lake
├── models/
│   └── lead_scoring_model.pkl
├── dashboards/
│   └── streamlit_app.py
├── mlflow/
├── requirements.txt
└── README.md
```

## 🧠 Model Pipeline Features

- Logistic Regression model with scikit-learn
- 5-fold cross-validation for performance estimation
- Hyperparameter tuning via GridSearchCV
- Versioned model saving (timestamped .pkl files)
- Evaluation metrics saved to JSON for monitoring

## 🔜 Next Steps

- [x] Complete ETL pipeline and convert to reusable scripts
- [x] Run exploratory analysis on customer behavior
- [x] Build segmentation or response model
- [ ] Deploy dashboard for insights
- [ ] Add unit tests for pipeline components
- [ ] Schedule daily pipeline using Airflow
- [ ] Containerize with Docker for local + cloud execution
