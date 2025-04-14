import pandas as pd
import os

# Load raw marketing data
df = pd.read_csv("data/raw/ifood_df.csv")

# Drop rows with any missing values
df = df.dropna()

# Optional: clean or rename columns if needed
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Optionally encode the target variable if needed
# For now, just keep as-is

# Save to processed directory
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/clean_marketing.csv", index=False)

print("✅ Cleaned data saved to data/processed/clean_marketing.csv")