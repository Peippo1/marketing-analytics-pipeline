import streamlit as st
import pandas as pd
import sys  # Ensures sys is available before attempting fallback

st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.write("🧪 Python executable:", sys.executable)
st.write("🧪 Python path:", sys.path)

# Try importing pymysql and handle the error if it's missing
try:
    import pymysql
except ModuleNotFoundError as e:
    st.error("❌ Required package 'pymysql' is not installed. Please check your environment.")
    st.stop()

from airflow.scripts.mysql_utils import get_customers_data


st.title("📊 Marketing Analytics Dashboard")
st.markdown("View cleaned customer data pulled live from MySQL.")

# Load data
try:
    df = get_customers_data()
    st.success("✅ Live data successfully loaded from Railway 🎉 — all systems go!")
    st.dataframe(df)
except Exception as e:
    st.error(f"Failed to load data: {e}")