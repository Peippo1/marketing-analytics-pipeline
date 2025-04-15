import streamlit as st
import pandas as pd
import joblib
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Marketing Response Dashboard", layout="wide")

# Title
st.title("📈 Marketing Analytics Dashboard")

# Load data
df = pd.read_csv("data/processed/clean_marketing.csv")
st.subheader("📊 Dataset Overview")
st.write(df.head())

# Basic stats
st.markdown("### 🧮 Summary Statistics")
st.write(df.describe())

# Visualizations
st.markdown("### 📈 Data Visualizations")

# 1. Distribution of Income
st.subheader("Income Distribution")
fig, ax = plt.subplots()
sns.histplot(df["Income"], bins=30, kde=True, ax=ax)
st.pyplot(fig)

# 2. Average Total Spend by Marital Status
st.subheader("Average Total Spend by Marital Status")
# Reverse one-hot encoding marital status
marital_cols = [col for col in df.columns if col.startswith("marital_")]
df["Marital_Status"] = df[marital_cols].idxmax(axis=1).str.replace("marital_", "")
spend_by_marital = df.groupby("Marital_Status")["MntTotal"].mean().sort_values()
fig2, ax2 = plt.subplots()
spend_by_marital.plot(kind="barh", ax=ax2)
ax2.set_xlabel("Average Total Spend")
st.pyplot(fig2)

# 3. Response Rate by Education Level
st.subheader("Response Rate by Education Level")
education_cols = [col for col in df.columns if col.startswith("education_")]
df["Education_Level"] = df[education_cols].idxmax(axis=1).str.replace("education_", "")
response_by_edu = df.groupby("Education_Level")["Response"].mean().sort_values()
fig3, ax3 = plt.subplots()
response_by_edu.plot(kind="barh", ax=ax3)
ax3.set_xlabel("Response Rate")
st.pyplot(fig3)

# Load latest model (sorted by timestamp in filename)
import os
model_files = sorted([f for f in os.listdir("models") if f.startswith("lead_scoring_model_")], reverse=True)
latest_model_path = f"models/{model_files[0]}" if model_files else None
if latest_model_path:
    model = joblib.load(latest_model_path)
    st.success(f"Loaded model: {latest_model_path}")
else:
    st.error("No model file found.")

# Input section
st.markdown("### 🧪 Make a Prediction")

with st.form("prediction_form"):
    income = st.slider("Income", 0, 150000, 60000, step=1000)
    kidhome = st.selectbox("Number of Kids at Home", [0, 1, 2])
    teenhome = st.selectbox("Number of Teens at Home", [0, 1, 2])
    recency = st.slider("Recency (days since last purchase)", 0, 100, 20)
    web = st.slider("Web Purchases", 0, 10, 4)
    catalog = st.slider("Catalog Purchases", 0, 10, 2)
    store = st.slider("Store Purchases", 0, 10, 5)
    visits = st.slider("Web Visits", 0, 20, 6)
    mnt_total = st.slider("Total Spend (MntTotal)", 0, 2000, 1000)
    mnt_regular = st.slider("Spend on Regular Products", 0, 2000, 700)
    marital_single = st.checkbox("Single", value=True)
    marital_married = st.checkbox("Married", value=False)
    education_grad = st.checkbox("Graduation", value=True)
    education_master = st.checkbox("Master", value=False)

    submitted = st.form_submit_button("Predict Response")

    if submitted and model:
        input_data = pd.DataFrame([{
            "Income": income,
            "Kidhome": kidhome,
            "Teenhome": teenhome,
            "Recency": recency,
            "NumWebPurchases": web,
            "NumCatalogPurchases": catalog,
            "NumStorePurchases": store,
            "NumWebVisitsMonth": visits,
            "MntTotal": mnt_total,
            "MntRegularProds": mnt_regular,
            "marital_Single": int(marital_single),
            "marital_Married": int(marital_married),
            "education_Graduation": int(education_grad),
            "education_Master": int(education_master)
        }])
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted Response: {'Yes' if prediction == 1 else 'No'}")

# Load metrics
st.markdown("### 📋 Model Evaluation Metrics")
try:
    with open("models/model_metrics.json") as f:
        metrics = json.load(f)
    st.json(metrics)
except:
    st.warning("No model_metrics.json found.")
