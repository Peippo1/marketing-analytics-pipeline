import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

from scripts.mysql_utils import get_mysql_engine

# Write cleaned data to MySQL
engine = get_mysql_engine()
df.to_sql("customers_cleaned", con=engine, if_exists="replace", index=False)
print("✅ Cleaned data written to MySQL: customers_cleaned table")