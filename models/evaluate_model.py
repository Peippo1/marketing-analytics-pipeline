"""
Evaluate the most recent trained model artifact against the processed dataset.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts" / "models"
DATA_PATH = BASE_DIR.parent / "data" / "processed" / "processed_marketing_data.csv"
CONFIG_PATH = BASE_DIR / "model_config.yaml"
METRICS_OUTPUT_DIR = BASE_DIR / "outputs"


def resolve_latest_model_path(artifacts_dir: Path = ARTIFACTS_DIR) -> Path:
    model_paths = sorted(artifacts_dir.glob("trained_model_*.pkl"))
    if not model_paths:
        raise FileNotFoundError(
            f"No trained model artifacts found in {artifacts_dir}. Run models/train_model.py first."
        )
    return model_paths[-1]


def load_model(model_path: Path):
    return joblib.load(model_path)


def load_data(data_path: Path) -> pd.DataFrame:
    return pd.read_csv(data_path)


def load_config(config_path: Path) -> dict:
    with config_path.open("r") as file:
        return yaml.safe_load(file)


def evaluate(model, features: pd.DataFrame, target: pd.Series) -> dict:
    predictions = model.predict(features)
    return {
        "accuracy": accuracy_score(target, predictions),
        "precision": precision_score(target, predictions, average="weighted"),
        "recall": recall_score(target, predictions, average="weighted"),
        "f1_score": f1_score(target, predictions, average="weighted"),
    }


def write_metrics(metrics: dict, model_path: Path) -> Path:
    METRICS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics_path = METRICS_OUTPUT_DIR / f"{model_path.stem}_evaluation.json"
    with metrics_path.open("w") as file:
        json.dump(metrics, file, indent=2)
    return metrics_path


def main():
    model_path = resolve_latest_model_path()
    model = load_model(model_path)
    dataset = load_data(DATA_PATH)
    config = load_config(CONFIG_PATH)

    target_column = config["data"]["target_column"]
    features = dataset.drop(columns=[target_column]).astype("float64")
    target = dataset[target_column].astype("float64")

    metrics = evaluate(model, features, target)

    print("\nModel Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value:.4f}")

    metrics_path = write_metrics(metrics, model_path)
    print(f"\nEvaluation metrics saved to {metrics_path}")


if __name__ == "__main__":
    main()
