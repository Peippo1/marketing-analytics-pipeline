from pathlib import Path
from typing import List, Optional
import os

import pandas as pd
from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "clean_marketing.csv"

app = FastAPI(title="Marketing Scoring API")


def _init_tracing() -> Optional[str]:
    """
    Initialize OpenTelemetry tracing if explicitly enabled.
    Safe no-op when OTEL_ENABLED is not set.
    """
    if os.getenv("OTEL_ENABLED", "").lower() not in {"1", "true", "yes"}:
        return None

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
    service_name = os.getenv("OTEL_SERVICE_NAME", "marketing-fastapi")

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    return endpoint


_init_tracing()


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
