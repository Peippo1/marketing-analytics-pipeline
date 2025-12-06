import pandas as pd

from utils.crm_clients import HubSpotClient, SalesforceClient


class StubHttp:
    def __init__(self):
        self.calls = []

    def post(self, url, headers=None, json=None, timeout=10):
        self.calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})

        class Resp:
            status_code = 201

            def raise_for_status(self):
                return None

        return Resp()


def test_salesforce_dry_run_builds_payload_without_http():
    client = SalesforceClient(instance_url="https://example.my.salesforce.com", http_client=StubHttp())
    rows = [
        {"LastName": "Doe", "Company": "ACME", "Email": "jane@example.com"},
        {"LastName": "Smith", "Company": "Beta", "Email": "john@example.com"},
    ]
    result = client.push_leads(rows, dry_run=True)

    assert result["sent"] == 2
    assert result["dry_run"] is True
    assert "composite/tree/Lead" in result["endpoint"]
    # ensure no network calls made
    assert client.http_client.calls == []


def test_salesforce_requires_required_fields():
    client = SalesforceClient(instance_url="https://example.my.salesforce.com")
    bad_rows = [{"Company": "ACME"}]  # missing LastName
    try:
        client.push_leads(bad_rows, dry_run=True)
    except ValueError as exc:
        assert "LastName" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing LastName")


def test_hubspot_dry_run_uses_batch_format():
    client = HubSpotClient(access_token="test", http_client=StubHttp())
    df = pd.DataFrame([{"email": "a@example.com"}, {"email": "b@example.com"}])

    result = client.push_contacts(df, dry_run=True)

    assert result["sent"] == 2
    assert result["dry_run"] is True
    assert "batch/create" in result["endpoint"]
    assert len(result["payload"]["inputs"]) == 2
    assert client.http_client.calls == []
