import os
import sys

# Add project root to sys.path for flexible imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Marketing Dashboard", layout="wide")
st.session_state["title_rendered"] = True
st.sidebar.title("Navigation")

st.write("🧪 Python executable:", sys.executable)
st.write("🧪 Python path:", sys.path)

# Try importing pymysql and handle the error if it's missing
try:
    import pymysql
except ModuleNotFoundError as e:
    st.error("❌ Required package 'pymysql' is not installed. Please check your environment.")
    st.stop()

from airflow.scripts.mysql_utils import get_customers_data
from utils.crm_clients import HubSpotClient, SalesforceClient


st.title("📊 Marketing Analytics Dashboard")
st.session_state["sidebar_initialized"] = True
st.markdown("View cleaned customer data pulled live from MySQL.")

# Load data
df = None
try:
    df = get_customers_data()
    st.success("✅ Live data successfully loaded from Railway 🎉 — all systems go!")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load data: {e}")


def _build_crm_records(dataframe):
    """Build minimal CRM-friendly records from the dataset."""
    records = []
    for idx, _ in dataframe.head(50).iterrows():
        records.append(
            {
                "LastName": f"Customer {idx}",
                "Company": "Marketing List",
                "Email": f"customer{idx}@example.com",
                "Recency": dataframe.loc[idx].get("Recency"),
                "Income": dataframe.loc[idx].get("Income"),
            }
        )
    return records


st.markdown("---")
st.subheader("🔗 CRM Sync (Salesforce / HubSpot)")
st.caption("Push a small batch of scored customers into your CRM. Defaults to dry-run for safety.")

crm_provider = st.selectbox("Select CRM", ["Salesforce", "HubSpot"])
dry_run = st.checkbox("Dry run (build payload only)", value=True)

if st.button("Push 20 customers to CRM"):
    if df is None or df.empty:
        st.error("No customer data available to push.")
    else:
        records = _build_crm_records(df)
        try:
            if crm_provider == "Salesforce":
                client = SalesforceClient()
                result = client.push_leads(records, dry_run=dry_run)
            else:
                client = HubSpotClient()
                result = client.push_contacts(records, dry_run=dry_run)

            if result.get("dry_run"):
                st.info(f"Dry run: prepared {result.get('sent', 0)} records. Endpoint: {result.get('endpoint')}")
            else:
                st.success(f"✅ Sent {result.get('sent', 0)} records to {crm_provider} (status {result.get('status_code')})")
        except Exception as exc:
            st.error(f"CRM push failed: {exc}")
