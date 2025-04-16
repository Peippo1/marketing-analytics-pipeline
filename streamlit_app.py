import streamlit as st
import pandas as pd
from scripts.mysql_utils import get_customers_data

st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.title("📊 Marketing Analytics Dashboard")
st.markdown("View cleaned customer data pulled live from MySQL.")

# Load data
try:
    df = get_customers_data()
    st.success("Data loaded successfully from MySQL.")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load data: {e}")
