"""
train_model.py

This script handles:
- Loading model configuration from YAML
- Loading preprocessed data
- Splitting data into training and testing sets
- Training a machine learning model
- Evaluating and saving the trained model
"""

import os
import pandas as pd
import joblib
import yaml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Import additional evaluation metrics for comprehensive model evaluation
from sklearn.metrics import precision_score, recall_score, f1_score
from datetime import datetime
import mlflow
import mlflow.sklearn

# Paths
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "model_config.yaml")
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/processed_marketing_data.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_config(config_path):
    """Load model configuration from a YAML file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def load_data(data_path):
    """Load preprocessed data from a CSV file. Raises an error if the file is not found."""
    return pd.read_csv(data_path)

def get_model(model_type, model_params):
    """Initialize and return a machine learning model."""
    if model_type == "RandomForestClassifier":
        return RandomForestClassifier(**model_params)
    elif model_type == "LogisticRegression":
        return LogisticRegression(**model_params)
    else:
        raise ValueError(f"Model type {model_type} is not supported yet.")

def main():
    try:
        # Step 1: Load configuration
        config = load_config(CONFIG_PATH)
        model_type = config.get("model", {}).get("type", "RandomForestClassifier")
        model_params = config.get("model", {}).get("params", {})

        data_config = config.get("data", {})
        target_column = data_config.get("target_column", "target")  # Default 'target'
        test_size = data_config.get("test_size", 0.2)               # Default 20% test split
        random_state = data_config.get("random_state", 42)          # Default seed

        # Check if processed data file exists
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"Processed data not found at {DATA_PATH}. Please run the ETL pipeline first.")

        # Step 2: Load data
        df = load_data(DATA_PATH)

        # Check if target column exists
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in data. Available columns: {list(df.columns)}")
        print(f"✅ Data loaded successfully with shape: {df.shape}")

        # Step 3: Prepare features and target
        X = df.drop(columns=[target_column]).astype('float64')
        y = df[target_column].astype('float64')

        # Step 4: Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"✅ Data split into training and test sets. Training size: {X_train.shape}, Test size: {X_test.shape}")

        # Step 5: Initialize and train the model
        model = get_model(model_type, model_params)
        print(f"✅ Initialized {model_type} model with params: {model_params}")

        mlflow.set_tracking_uri("http://127.0.0.1:5001")

        with mlflow.start_run():
            mlflow.log_params(model_params)
            model.fit(X_train, y_train)
            print(f"✅ Model training completed.")

            # Step 6: Evaluate the model
            y_pred = model.predict(X_test)
            input_example = X_test.iloc[:1].astype('float64')
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Test Accuracy: {accuracy:.4f}")

            # Calculate additional evaluation metrics to get a well-rounded view of model performance
            # Precision: proportion of positive identifications that were actually correct
            # Recall: proportion of actual positives that were identified correctly
            # F1 Score: harmonic mean of precision and recall, balances the two
            precision = precision_score(y_test, y_pred, average="weighted")
            recall = recall_score(y_test, y_pred, average="weighted")
            f1 = f1_score(y_test, y_pred, average="weighted")

            # Print metrics for visibility and quick inspection
            print(f"Test Precision: {precision:.4f}")
            print(f"Test Recall: {recall:.4f}")
            print(f"Test F1 Score: {f1:.4f}")

            # Log evaluation metrics to MLflow for experiment tracking and comparison
            mlflow.log_metrics({
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            })

            # Step 7: Save the trained model
            # Create a timestamp for the model filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_filename = f"trained_model_{timestamp}.pkl"
            model_output_path = os.path.join(os.path.dirname(__file__), "artifacts", "models", model_filename)

            os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

            joblib.dump(model, model_output_path)
            print(f"✅ Trained model saved successfully at: {model_output_path}")

            # Save evaluation metrics as JSON alongside the model
            import json

            metrics_filename = f"trained_model_{timestamp}_metrics.json"
            metrics_output_path = os.path.join(os.path.dirname(__file__), "artifacts", "models", metrics_filename)

            metrics_dict = {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }

            with open(metrics_output_path, "w") as f:
                json.dump(metrics_dict, f, indent=4)

            print(f"✅ Evaluation metrics saved successfully at: {metrics_output_path}")

            mlflow.sklearn.log_model(model, artifact_path="model", input_example=input_example)

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
