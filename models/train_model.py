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
from sklearn.metrics import accuracy_score

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
        X = df.drop(columns=[target_column])
        y = df[target_column]

        # Step 4: Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"✅ Data split into training and test sets. Training size: {X_train.shape}, Test size: {X_test.shape}")

        # Step 5: Initialize and train the model
        model = get_model(model_type, model_params)
        print(f"✅ Initialized {model_type} model with params: {model_params}")
        model.fit(X_train, y_train)
        print(f"✅ Model training completed.")

        # Step 6: Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {accuracy:.4f}")

        # Step 7: Save the trained model
        model_output_path = os.path.join(OUTPUT_DIR, "trained_model.pkl")
        joblib.dump(model, model_output_path)
        print(f"✅ Trained model saved successfully at: {model_output_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
