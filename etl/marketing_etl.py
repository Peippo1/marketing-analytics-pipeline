# marketing_etl.py

import pandas as pd
import os
import zipfile

# ETL script that extracts marketing data from a zipped archive, transforms it, and saves the processed file.
def run_marketing_etl():
    # 1. Extract
    zip_path = 'data/raw/marketing-data.zip'
    extract_path = 'data/raw/'

    # Unzip the file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Assuming the extracted CSV file name (update if necessary)
    extracted_csv_path = os.path.join(extract_path, 'marketing_data.csv')  # update this if the file has a different name

    # Load the extracted CSV
    df = pd.read_csv(extracted_csv_path)

    # 2. Transform
    df = df.dropna()
    if 'clicks' in df.columns and 'impressions' in df.columns:
        df['CTR'] = df['clicks'] / df['impressions']

    # 3. Load
    processed_data_path = 'data/processed/processed_marketing_data.csv'
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df.to_csv(processed_data_path, index=False)

    print(f"Processed data saved to {processed_data_path}")