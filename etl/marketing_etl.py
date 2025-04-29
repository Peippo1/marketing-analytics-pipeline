
# marketing_etl.py

"""
This ETL script prepares marketing data from the Ifood dataset for machine learning.

Overview:
- Loads data from either a raw CSV file ('ifood_df.csv') or, if not found, extracts it from a ZIP archive ('ifood_data.zip').
- Cleans the dataset by removing duplicates and missing values.
- Optionally engineers additional features (e.g., extracting 'year' and 'month' from a 'date' column if present).
- Saves the processed dataset as 'data/processed/processed_marketing_data.csv'.

Designed for flexibility in local development and reproducibility in GitHub-hosted workflows.
"""

import pandas as pd
import os
import zipfile

def run_marketing_etl():
    """
    Run the ETL pipeline:
    - Attempts to load 'ifood_df.csv' from raw data
    - If not found, checks for 'ifood_data.zip' and extracts it
    - Cleans data (duplicates, missing values)
    - Optional feature engineering
    - Saves processed CSV
    """
    print("Starting ETL for ifood_df.csv...")

    # Step 1: Attempt to locate raw CSV.
    # If not found, look for a ZIP archive and extract it.
    # This makes the pipeline flexible for users who upload zipped datasets (e.g., on GitHub).

    # Step 1: Check for CSV or ZIP
    input_csv_path = 'data/raw/ifood_df.csv'
    zip_path = 'data/raw/ifood_data.zip'

    if not os.path.exists(input_csv_path):
        if os.path.exists(zip_path):
            print("CSV not found. Found ZIP archive. Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('data/raw/')
            # After extraction, check again if the expected CSV now exists.
            # If it still doesn't, raise an error with a clear message.
            if not os.path.exists(input_csv_path):
                raise FileNotFoundError(f"Extracted CSV still not found at {input_csv_path}")
            print("Extraction completed.")
        else:
            raise FileNotFoundError(f"Input CSV not found at {input_csv_path} and no ZIP file found at {zip_path}")

    # Load CSV into DataFrame
    df = pd.read_csv(input_csv_path)
    print(f"Data loaded with shape: {df.shape}")

    # Step 2: Clean
    df = df.drop_duplicates()
    print(f"Data after dropping duplicates: {df.shape}")

    df = df.dropna()
    print(f"Data after dropping missing values: {df.shape}")

    # Step 3: Optional feature engineering
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        print("Extracted 'year' and 'month' from 'date' column.")

    # Step 4: Save
    processed_data_path = 'data/processed/processed_marketing_data.csv'
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)

    df.to_csv(processed_data_path, index=False)
    print(f"✅ Processed data saved to {processed_data_path}")

if __name__ == "__main__":
    # Run ETL when script is executed
    run_marketing_etl()