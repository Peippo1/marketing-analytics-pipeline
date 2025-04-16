import streamlit as st
import pandas as pd
import joblib
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.mysql_utils import get_customers_data

# Set page config
st.set_page_config(page_title="Marketing Response Dashboard", layout="wide")

# Title
st.title("📈 Marketing Analytics Dashboard")

# Load data
df = pd.read_csv("data/processed/clean_marketing.csv")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
min_income, max_income = int(df["Income"].min()), int(df["Income"].max())
income_range = st.sidebar.slider("Income Range", min_income, max_income, (min_income, max_income))

marital_cols = [col for col in df.columns if col.startswith("marital_")]
df["Marital_Status"] = df[marital_cols].idxmax(axis=1).str.replace("marital_", "")
marital_options = df["Marital_Status"].unique().tolist()
selected_marital = st.sidebar.multiselect("Marital Status", marital_options, default=marital_options)

show_respondents_only = st.sidebar.checkbox("Only include respondents (Response = 1)")

# Sidebar navigation (must come before conditionals)
page = st.sidebar.radio("🔍 Navigation", ["Overview", "Visualizations", "Predict", "Database View"])

# Apply filters
df_filtered = df[
    (df["Income"] >= income_range[0]) &
    (df["Income"] <= income_range[1]) &
    (df["Marital_Status"].isin(selected_marital))
]
if show_respondents_only:
    df_filtered = df_filtered[df_filtered["Response"] == 1]

if page == "Overview":
    st.subheader("📊 Dataset Overview")
    st.write(df.head())

    # Summary stats
    st.markdown("### 🧮 Summary Statistics")
    st.write(df_filtered.describe())

    # Export section
    st.markdown("### 📤 Download Filtered Data")
    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_marketing_data.csv",
        mime="text/csv"
    )

elif page == "Visualizations":
    st.markdown("### 📈 Data Visualizations")

    # 1. Distribution of Income
    st.subheader("Income Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df_filtered["Income"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

    # 2. Average Total Spend by Marital Status
    st.subheader("Average Total Spend by Marital Status")
    spend_by_marital = df_filtered.groupby("Marital_Status")["MntTotal"].mean().sort_values()
    fig2, ax2 = plt.subplots()
    spend_by_marital.plot(kind="barh", ax=ax2)
    ax2.set_xlabel("Average Total Spend")
    st.pyplot(fig2)

    # 3. Response Rate by Education Level
    st.subheader("Response Rate by Education Level")
    education_cols = [col for col in df.columns if col.startswith("education_")]
    df_filtered["Education_Level"] = df_filtered[education_cols].idxmax(axis=1).str.replace("education_", "")
    response_by_edu = df_filtered.groupby("Education_Level")["Response"].mean().sort_values()
    fig3, ax3 = plt.subplots()
    response_by_edu.plot(kind="barh", ax=ax3)
    ax3.set_xlabel("Response Rate")
    st.pyplot(fig3)

elif page == "Predict":
    st.markdown("### 🧪 Make a Prediction")

    # Load latest model
    model = None
    model_files = sorted([f for f in os.listdir("models") if f.startswith("lead_scoring_model_")], reverse=True)

    # Try to load the latest timestamped model first
    if model_files:
        latest_model_path = f"models/{model_files[0]}"
        model = joblib.load(latest_model_path)
        st.success(f"Loaded model: {latest_model_path}")
    # Fallback to static file
    elif os.path.exists("models/lead_scoring_model.pkl"):
        model = joblib.load("models/lead_scoring_model.pkl")
        st.warning("Loaded fallback model: models/lead_scoring_model.pkl")
    else:
        st.error("No model file found.")

    # Prediction form in two columns
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            income = st.slider("Income", 0, 150000, 60000, step=1000)
            kidhome = st.selectbox("Number of Kids at Home", [0, 1, 2])
            teenhome = st.selectbox("Number of Teens at Home", [0, 1, 2])
            recency = st.slider("Recency (days since last purchase)", 0, 100, 20)
            web = st.slider("Web Purchases", 0, 10, 4)
            catalog = st.slider("Catalog Purchases", 0, 10, 2)

        with col2:
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

    # Metrics section
    st.markdown("### 📋 Model Evaluation Metrics")
    try:
        with open("models/model_metrics.json") as f:
            metrics = json.load(f)
        st.json(metrics)
    except:
        st.warning("No model_metrics.json found.")

elif page == "Database View":
    # ----------------------------------------
    # 📂 Database View Section
    # ----------------------------------------
    # This section adds a new page in the dashboard that connects to the MySQL database
    # and displays the contents of the `customers_cleaned` table in a Streamlit dataframe.
    
    st.title("📂 Customers from MySQL")

    # Use a spinner while the data is being fetched
    with st.spinner("Fetching records from MySQL..."):
        try:
            # Load customer data from MySQL using the shared utility function
            df_db = get_customers_data()

            # Display the dataframe interactively in the app
            st.dataframe(df_db)

        except Exception as e:
            # Display a friendly error if the fetch fails
            st.error(f"Error loading data: {e}")
