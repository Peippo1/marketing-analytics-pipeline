# tests/test_sheets_sync.py
import pandas as pd
from utils.sheets_sync import sync_to_google_sheets
import streamlit as st

def test_sync_to_sheets():
    df = pd.DataFrame({
        "customer_id": [1, 2],
        "score": [0.87, 0.45]
    })
    success = sync_to_google_sheets(df, "Test_Scored_Customers", st.secrets["gcp_service_account"])
    assert success