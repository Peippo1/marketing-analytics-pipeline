import streamlit as st
import pandas as pd
import pymysql
from scripts.mysql_utils import get_customers_data
import sys  # Added import to avoid module import error

st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.title("📊 Marketing Analytics Dashboard")
st.markdown("View cleaned customer data pulled live from MySQL.")

# Load data
try:
    df = get_customers_data()
    st.success("✅ Live data successfully loaded from Railway 🎉")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load data: {e}")
