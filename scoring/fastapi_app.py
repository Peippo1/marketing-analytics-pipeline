from pathlib import Path
from typing import List

import pandas as pd
from fastapi import FastAPI

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "clean_marketing.csv"

app = FastAPI(title="Marketing Scoring API")


@app.get("/health")
def health_check() -> dict:
    """Simple health endpoint for liveness probes."""
    return {"status": "ok"}


@app.get("/customers")
def list_customers(limit: int = 10) -> List[dict]:
    """
    Return a lightweight customer listing for UI smoke tests.
    Falls back to a few synthetic rows if the local data file is missing.
    """
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH).reset_index(drop=True)
        df.insert(0, "customer_id", df.index + 1)
        rows = df.head(limit)
    else:
        rows = pd.DataFrame(
            [
                {"customer_id": 1, "Income": 58000, "Recency": 10},
                {"customer_id": 2, "Income": 42000, "Recency": 24},
            ]
        )
    return rows.to_dict(orient="records")
