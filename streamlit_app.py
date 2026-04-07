import os
import sys

# Add project root to sys.path for flexible imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import pandas as pd
import streamlit as st

# Try importing pymysql and handle the error if it's missing
try:
    import pymysql  # noqa: F401
except ModuleNotFoundError:
    st.set_page_config(page_title="CampaignForge AI Dashboard", layout="wide")
    st.error("Required package 'pymysql' is not installed. Please check your environment.")
    st.stop()

from airflow.scripts.mysql_utils import get_customers_data
from utils.crm_clients import HubSpotClient, SalesforceClient


st.set_page_config(page_title="CampaignForge AI Dashboard", layout="wide")
st.session_state["title_rendered"] = True
st.session_state["sidebar_initialized"] = True


def render_styles():
    st.markdown(
        """
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(247, 205, 70, 0.18), transparent 30%),
                    radial-gradient(circle at top right, rgba(53, 122, 189, 0.14), transparent 28%),
                    linear-gradient(180deg, #f7f3ea 0%, #eef2f7 100%);
            }
            .hero-card {
                background: linear-gradient(135deg, #10233f 0%, #1f4a73 55%, #d8a73e 140%);
                color: #f8f5ef;
                padding: 1.6rem 1.8rem;
                border-radius: 20px;
                box-shadow: 0 18px 45px rgba(16, 35, 63, 0.16);
                margin-bottom: 1rem;
            }
            .hero-kicker {
                font-size: 0.8rem;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                opacity: 0.78;
                margin-bottom: 0.6rem;
            }
            .hero-title {
                font-size: 2.2rem;
                font-weight: 700;
                line-height: 1.1;
                margin-bottom: 0.65rem;
            }
            .hero-copy {
                max-width: 52rem;
                font-size: 1rem;
                line-height: 1.55;
                opacity: 0.94;
            }
            .info-card {
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(16, 35, 63, 0.08);
                border-radius: 16px;
                padding: 1rem 1.1rem;
                box-shadow: 0 10px 24px rgba(16, 35, 63, 0.07);
            }
            .section-label {
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                color: #7b5b16;
                margin-bottom: 0.4rem;
                font-weight: 700;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_customer_data():
    try:
        return get_customers_data(), None
    except Exception as exc:
        return None, exc


def build_crm_records(dataframe: pd.DataFrame):
    records = []
    for idx, _ in dataframe.head(20).iterrows():
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


def render_sidebar():
    st.sidebar.title("Operator Controls")
    st.sidebar.caption("Use this dashboard as a quick demo of campaign data visibility and CRM handoff.")

    crm_provider = st.sidebar.selectbox("CRM Provider", ["Salesforce", "HubSpot"])
    dry_run = st.sidebar.checkbox("Dry run only", value=True)

    if os.getenv("STREAMLIT_DEBUG", "").lower() in {"1", "true", "yes"}:
        st.sidebar.write("Python executable:", sys.executable)
        st.sidebar.write("Python path:", sys.path)

    return crm_provider, dry_run


def render_hero(dataframe: pd.DataFrame | None):
    row_count = int(len(dataframe)) if dataframe is not None else 0
    avg_income = float(dataframe["Income"].mean()) if dataframe is not None and "Income" in dataframe else 0.0
    avg_recency = float(dataframe["Recency"].mean()) if dataframe is not None and "Recency" in dataframe else 0.0

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">CampaignForge AI</div>
            <div class="hero-title">Campaign Intelligence Dashboard</div>
            <div class="hero-copy">
                A lightweight operations view for reviewing campaign and customer segments, surfacing
                lead-scoring inputs, and demonstrating downstream CRM sync workflows from one interface.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Customer Rows", f"{row_count:,}")
    col2.metric("Average Income", f"{avg_income:,.0f}")
    col3.metric("Average Recency", f"{avg_recency:.1f}")


def render_dataset_panel(dataframe: pd.DataFrame | None, load_error: Exception | None):
    st.markdown('<div class="section-label">Dataset Preview</div>', unsafe_allow_html=True)
    if load_error is not None:
        st.error(f"Failed to load customer data: {load_error}")
        return

    if dataframe is None or dataframe.empty:
        st.warning("No customer data is currently available.")
        return

    preview_col, notes_col = st.columns([1.6, 1])
    with preview_col:
        st.dataframe(dataframe.head(25), use_container_width=True)
    with notes_col:
        st.markdown(
            """
            <div class="info-card">
                <strong>What this demonstrates</strong><br><br>
                Cleaned customer records flowing into a buyer-friendly dashboard layer that can support
                reporting, campaign analytics demos, and lightweight operational actions.
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_crm_panel(dataframe: pd.DataFrame | None, crm_provider: str, dry_run: bool):
    st.markdown("---")
    st.markdown('<div class="section-label">CRM Sync Demo</div>', unsafe_allow_html=True)
    st.subheader("Push a sample customer batch to Salesforce or HubSpot")
    st.caption("Use dry-run mode for demos so you can show the integration flow without sending live records.")

    if st.button("Push 20 customers to CRM", type="primary"):
        if dataframe is None or dataframe.empty:
            st.error("No customer data available to push.")
            return

        records = build_crm_records(dataframe)
        try:
            if crm_provider == "Salesforce":
                client = SalesforceClient()
                result = client.push_leads(records, dry_run=dry_run)
            else:
                client = HubSpotClient()
                result = client.push_contacts(records, dry_run=dry_run)

            if result.get("dry_run"):
                st.info(
                    f"Dry run complete: prepared {result.get('sent', 0)} records for {crm_provider}. "
                    f"Endpoint: {result.get('endpoint')}"
                )
            else:
                st.success(
                    f"Sent {result.get('sent', 0)} records to {crm_provider} "
                    f"(status {result.get('status_code')})."
                )
        except Exception as exc:
            st.error(f"CRM push failed: {exc}")


def main():
    render_styles()
    crm_provider, dry_run = render_sidebar()
    dataframe, load_error = load_customer_data()
    render_hero(dataframe)
    render_dataset_panel(dataframe, load_error)
    render_crm_panel(dataframe, crm_provider, dry_run)


main()
