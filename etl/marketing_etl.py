# marketing_etl.py

"""
ETL script for marketing data:
- Extracts zipped data
- Loads into a DataFrame
- Cleans and preprocesses
- Basic feature engineering (CTR, year, month)
- Saves processed CSV
"""

import pandas as pd
import os
import zipfile

def run_marketing_etl():
    """
    Run the ETL pipeline:
    - Extracts data from zip file
    - Loads into pandas DataFrame
    - Cleans data (duplicates, missing values, invalid impressions)
    - Engineers features
    - Saves processed CSV
    """
    # 1. Extract
    print("Starting extraction...")
    zip_path = 'data/raw/marketing-data.zip'
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Zip file not found at {zip_path}")
    extract_path = 'data/raw/'

    # Unzip marketing data
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Extraction completed.")

    extracted_csv_path = os.path.join(extract_path, 'marketing_data.csv')  # path to extracted CSV

    if not os.path.exists(extracted_csv_path):
        raise FileNotFoundError(f"Extracted CSV not found at {extracted_csv_path}")

    # Load CSV into DataFrame
    df = pd.read_csv(extracted_csv_path)
    print(f"Data loaded with shape {df.shape}.")

    # 2. Transform
    print("Starting transformation...")

    # Remove duplicate rows
    df = df.drop_duplicates()
    print(f"Data after dropping duplicates: {df.shape}")

    # Drop rows with any missing values
    df = df.dropna()
    print(f"Data after dropping missing values: {df.shape}")

    # Remove rows with zero or negative impressions
    if 'impressions' in df.columns:
        df = df[df['impressions'] > 0]
        print(f"Data after removing zero impressions: {df.shape}")

    # Feature engineering: Calculate CTR
    if 'clicks' in df.columns and 'impressions' in df.columns:
        df['CTR'] = df['clicks'] / df['impressions']

    # Feature engineering: Extract year and month from 'date'
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        print("Extracted 'year' and 'month' from 'date'.")

    # 3. Load
    processed_data_path = 'data/processed/processed_marketing_data.csv'
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)

    print(f"Saving processed data to {processed_data_path}...")
    # Save processed data
    df.to_csv(processed_data_path, index=False)

    print(f"Processed data saved to {processed_data_path}")

if __name__ == "__main__":
    # Run ETL when script is executed
    run_marketing_etl()