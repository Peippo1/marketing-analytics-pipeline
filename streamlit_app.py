import streamlit as st
import pandas as pd
import sys  # Ensures sys is available before attempting fallback

# Try importing pymysql and handle the error if it's missing
try:
    import pymysql
except ModuleNotFoundError as e:
    st.error("❌ Required package 'pymysql' is not installed. Please check your environment.")
    st.stop()

from scripts.mysql_utils import get_customers_data

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

import subprocess
installed_packages = subprocess.check_output(["pip", "freeze"]).decode("utf-8")
st.text(installed_packages)