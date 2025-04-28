"""
Evaluate a trained model on validation/test data.
"""

import pandas as pd
import pickle
import yaml
import json
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 1. Define paths
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "../artifacts/trained_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/clean_marketing.csv")
CONFIG_PATH = os.path.join(BASE_DIR, "../models/model_config.yaml")
METRICS_PATH = os.path.join(BASE_DIR, "../data/metrics/metrics.json")

# 2. Load the trained model
def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

# 3. Load the data
def load_data(data_path):
    return pd.read_csv(data_path)

# 4. Load model config
def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# 5. Evaluate model
def evaluate(model, X, y):
    preds = model.predict(X)
    return {
        "accuracy": accuracy_score(y, preds),
        "precision": precision_score(y, preds),
        "recall": recall_score(y, preds),
        "f1": f1_score(y, preds),
    }

# 6. Main
def main():
    model = load_model(MODEL_PATH)
    df = load_data(DATA_PATH)
    config = load_config(CONFIG_PATH)

    target_column = config["data"]["target_column"]

    X = df.drop(columns=[target_column])
    y = df[target_column]

    metrics = evaluate(model, X, y)

    # Print metrics nicely
    print("\nModel Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key.capitalize()}: {value:.4f}")

    # Save metrics
    os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"\nEvaluation metrics saved to {METRICS_PATH}!")

if __name__ == "__main__":
    main()