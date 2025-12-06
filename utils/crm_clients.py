"""
Lightweight CRM clients for Salesforce and HubSpot.
Designed to work with simple customer dictionaries or pandas DataFrames.
Network calls are optional (dry_run=True) to keep local/dev runs safe.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List, MutableMapping, Sequence

import pandas as pd
import requests


def _to_records(rows: Sequence[MutableMapping] | pd.DataFrame) -> List[MutableMapping]:
    """Normalize input rows into a list of dicts."""
    if isinstance(rows, pd.DataFrame):
        return rows.to_dict(orient="records")
    return [dict(r) for r in rows]


@dataclass
class SalesforceClient:
    instance_url: str | None = None
    access_token: str | None = None
    api_version: str = "v60.0"
    http_client: requests.sessions.Session | None = None

    def __post_init__(self):
        self.instance_url = self.instance_url or os.getenv("SALESFORCE_INSTANCE_URL")
        self.access_token = self.access_token or os.getenv("SALESFORCE_ACCESS_TOKEN")
        if self.instance_url:
            self.instance_url = self.instance_url.rstrip("/")
        self.http_client = self.http_client or requests.Session()

    def _build_payload(self, records: Iterable[MutableMapping]) -> dict:
        """
        Build a composite tree payload for Lead upsert.
        Salesforce requires LastName and Company; callers must provide them.
        """
        processed = []
        for idx, rec in enumerate(records):
            record = dict(rec)
            if "LastName" not in record or "Company" not in record:
                raise ValueError("Salesforce lead requires 'LastName' and 'Company'")
            processed.append(
                {
                    "attributes": {"type": "Lead", "referenceId": f"ref{idx}"},
                    **record,
                }
            )
        return {"records": processed}

    def push_leads(self, rows: Sequence[MutableMapping] | pd.DataFrame, dry_run: bool = True) -> dict:
        """Push leads via composite tree API. Returns response metadata or payload when dry_run."""
        records = _to_records(rows)
        if not records:
            return {"sent": 0, "dry_run": dry_run}

        payload = self._build_payload(records)
        endpoint = f"{self.instance_url}/services/data/{self.api_version}/composite/tree/Lead"

        if dry_run:
            return {"sent": len(payload["records"]), "dry_run": True, "endpoint": endpoint, "payload": payload}

        if not self.instance_url or not self.access_token:
            raise RuntimeError("Salesforce credentials missing (SALESFORCE_INSTANCE_URL/SALESFORCE_ACCESS_TOKEN)")

        resp = self.http_client.post(
            endpoint,
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        return {"sent": len(payload["records"]), "dry_run": False, "status_code": resp.status_code}


@dataclass
class HubSpotClient:
    access_token: str | None = None
    http_client: requests.sessions.Session | None = None

    def __post_init__(self):
        self.access_token = self.access_token or os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.http_client = self.http_client or requests.Session()

    def _build_payload(self, records: Iterable[MutableMapping]) -> dict:
        processed = []
        for rec in records:
            properties = dict(rec)
            processed.append({"properties": properties})
        return {"inputs": processed}

    def push_contacts(self, rows: Sequence[MutableMapping] | pd.DataFrame, dry_run: bool = True) -> dict:
        """Push contacts in batch. Returns response metadata or payload when dry_run."""
        records = _to_records(rows)
        if not records:
            return {"sent": 0, "dry_run": dry_run}

        payload = self._build_payload(records)
        endpoint = "https://api.hubapi.com/crm/v3/objects/contacts/batch/create"

        if dry_run:
            return {"sent": len(payload["inputs"]), "dry_run": True, "endpoint": endpoint, "payload": payload}

        if not self.access_token:
            raise RuntimeError("HubSpot credentials missing (HUBSPOT_ACCESS_TOKEN)")

        resp = self.http_client.post(
            endpoint,
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        return {"sent": len(payload["inputs"]), "dry_run": False, "status_code": resp.status_code}
