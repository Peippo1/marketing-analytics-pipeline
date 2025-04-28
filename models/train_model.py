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
    """Load preprocessed data from a CSV file."""
    return pd.read_csv(data_path)

def get_model(model_type, model_params):
    """Initialize and return a machine learning model."""
    if model_type == "RandomForestClassifier":
        return RandomForestClassifier(**model_params)
    else:
        raise ValueError(f"Model type {model_type} is not supported yet.")

def main():
    # Step 1: Load configuration
    config = load_config(CONFIG_PATH)
    model_type = config.get("model", {}).get("type", "RandomForestClassifier")
    model_params = config.get("model", {}).get("params", {})

    data_config = config.get("data", {})
    target_column = data_config.get("target_column", "target")  # Default 'target'
    test_size = data_config.get("test_size", 0.2)               # Default 20% test split
    random_state = data_config.get("random_state", 42)          # Default seed

    # Step 2: Load data
    df = load_data(DATA_PATH)

    # Step 3: Prepare features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Step 4: Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Step 5: Initialize and train the model
    model = get_model(model_type, model_params)
    model.fit(X_train, y_train)

    # Step 6: Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy:.4f}")

    # Step 7: Save the trained model
    model_output_path = os.path.join(OUTPUT_DIR, "trained_model.pkl")
    joblib.dump(model, model_output_path)
    print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    main()
