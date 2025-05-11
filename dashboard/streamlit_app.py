import streamlit as st
import os
import joblib
import pandas as pd
from google.oauth2.service_account import Credentials

# Set Streamlit page configuration
st.set_page_config(page_title="Marketing Analytics Dashboard", layout="wide")

# Title
st.title("📊 Marketing Analytics - Model Dashboard")

# Sidebar
st.sidebar.header("Navigation")

# Navigation options
app_mode = st.sidebar.selectbox("Choose Section:", ["🏠 Home", "📈 View Models", "📝 Upload & Score"])

# Home Page
if app_mode == "🏠 Home":
    st.subheader("Welcome!")
    st.write("""
    This dashboard allows you to:
    - View trained machine learning models
    - Select and compare model evaluation metrics
    - Upload new customer datasets and score them
    """)

# View Models Page
elif app_mode == "📈 View Models":
    st.subheader("Available Trained Models")
    
    models_dir = "models/artifacts/models"
    if os.path.exists(models_dir):
        model_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl")]
        if model_files:
            selected_model = st.selectbox("Select a Model File", model_files)
            model_path = os.path.join(models_dir, selected_model)
            model = joblib.load(model_path)
            st.success(f"Model `{selected_model}` loaded successfully!")
            st.write(model)

            # Display dynamic evaluation metrics
            metrics_file = selected_model.replace(".pkl", "_metrics.json")
            metrics_path = os.path.join(models_dir, metrics_file)

            if os.path.exists(metrics_path):
                import json
                with open(metrics_path, "r") as f:
                    metrics = json.load(f)

                with st.expander("📊 Model Evaluation Metrics", expanded=True):
                    st.metric(label="Accuracy", value=f"{metrics.get('accuracy', 0)*100:.2f}%")
                    st.metric(label="Precision", value=f"{metrics.get('precision', 0)*100:.2f}%")
                    st.metric(label="Recall", value=f"{metrics.get('recall', 0)*100:.2f}%")
                    st.metric(label="F1 Score", value=f"{metrics.get('f1_score', 0)*100:.2f}%")
            else:
                st.warning("Metrics file not found for the selected model.")
        else:
            st.warning("No trained model files found.")
    else:
        st.error("Models directory not found. Please train a model first.")

# Upload & Score Page
elif app_mode == "📝 Upload & Score":
    st.subheader("Upload Customer Data and Score")

    # Upload CSV
    uploaded_file = st.file_uploader("Upload a CSV file for scoring", type=["csv"])
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.write("Uploaded Data Preview:")
        st.dataframe(df_upload.head())

        # Select Model for Scoring
        models_dir = "models/artifacts/models"
        model_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl")]
        if model_files:
            selected_model = st.selectbox("Select a Model to Score", model_files)
            model_path = os.path.join(models_dir, selected_model)
            model = joblib.load(model_path)

            # Predict Button
            if st.button("Predict"):
                try:
                    # Check if the uploaded data columns match what the model expects
                    expected_features = model.n_features_in_
                    if df_upload.shape[1] != expected_features:
                        st.error(f"Uploaded data has {df_upload.shape[1]} features but the model expects {expected_features}. Please check your file.")
                    elif hasattr(model, 'feature_names_in_'):
                        model_features = list(model.feature_names_in_)
                        upload_features = list(df_upload.columns)
                        if set(model_features) != set(upload_features):
                            st.error("Uploaded data columns do not match the model's expected features. Please review the differences below:")

                            missing_in_upload = list(set(model_features) - set(upload_features))
                            extra_in_upload = list(set(upload_features) - set(model_features))

                            col1, col2 = st.columns(2)
                            with col1:
                                st.subheader("🔹 Expected Features")
                                st.write(model_features)
                                if missing_in_upload:
                                    st.warning(f"Missing in upload: {missing_in_upload}")
                            with col2:
                                st.subheader("🔸 Uploaded Features")
                                st.write(upload_features)
                                if extra_in_upload:
                                    st.warning(f"Unexpected in upload: {extra_in_upload}")

                            with st.expander("🔍 Uploaded Data Preview (First 5 Rows)"):
                                st.dataframe(df_upload.head())
                        else:
                            st.success("✅ Feature match successful! Model and data are aligned.")
                            df_upload = df_upload[model_features]  # Ensure correct order
                            predictions = model.predict(df_upload)
                            df_upload["Prediction"] = predictions
                            st.success("Predictions completed successfully!")
                            st.write("Scored Data Preview:")
                            st.dataframe(df_upload.head())

                            # Allow download
                            csv = df_upload.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="Download Scored Data",
                                data=csv,
                                file_name="scored_customers.csv",
                                mime="text/csv",
                            )

                            # Optional: Sync to Google Sheets
                            if st.button("Sync to Google Sheets"):
                                try:
                                    import gspread
                                    from google.oauth2.service_account import Credentials

                                    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
                                    client = gspread.authorize(creds)

                                    # Create or open spreadsheet
                                    sheet_name = "Scored_Customers"
                                    try:
                                        sheet = client.open(sheet_name).sheet1
                                    except gspread.SpreadsheetNotFound:
                                        sheet = client.create(sheet_name).sheet1

                                    # Clear and upload new data
                                    sheet.clear()
                                    sheet.update([df_upload.columns.values.tolist()] + df_upload.values.tolist())
                                    st.success(f"Synced to Google Sheet: {sheet_name}")
                                except Exception as e:
                                    st.error(f"Google Sheets sync failed: {e}")
                    else:
                        predictions = model.predict(df_upload)
                        df_upload["Prediction"] = predictions
                        st.success("Predictions completed successfully!")
                        st.write("Scored Data Preview:")
                        st.dataframe(df_upload.head())

                        # Allow download
                        csv = df_upload.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Scored Data",
                            data=csv,
                            file_name="scored_customers.csv",
                            mime="text/csv",
                        )

                        # Optional: Sync to Google Sheets
                        if st.button("Sync to Google Sheets"):
                            try:
                                import gspread
                                from google.oauth2.service_account import Credentials

                                creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
                                client = gspread.authorize(creds)

                                # Create or open spreadsheet
                                sheet_name = "Scored_Customers"
                                try:
                                    sheet = client.open(sheet_name).sheet1
                                except gspread.SpreadsheetNotFound:
                                    sheet = client.create(sheet_name).sheet1

                                # Clear and upload new data
                                sheet.clear()
                                sheet.update([df_upload.columns.values.tolist()] + df_upload.values.tolist())
                                st.success(f"Synced to Google Sheet: {sheet_name}")
                            except Exception as e:
                                st.error(f"Google Sheets sync failed: {e}")
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
        else:
            st.warning("No trained models available for scoring. Please train a model first.")
