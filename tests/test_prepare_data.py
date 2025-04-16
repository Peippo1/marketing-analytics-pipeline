import pandas as pd
import pytest

# Load the cleaned dataset once for all tests
@pytest.fixture
def cleaned_data():
    # Load the preprocessed CSV from the processed data directory
    return pd.read_csv("data/processed/clean_marketing.csv")

# Ensure there are no missing values in the cleaned dataset
def test_no_null_values(cleaned_data):
    assert cleaned_data.isnull().sum().sum() == 0, "There are null values in the cleaned data."

# Check that all the expected columns are present after preprocessing
def test_expected_columns_exist(cleaned_data):
    expected_columns = [
        "Income", "Kidhome", "Teenhome", "Recency", "MntTotal", "MntRegularProds",
        "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth",
        "Response"
    ]
    missing = [col for col in expected_columns if col not in cleaned_data.columns]
    assert not missing, f"Missing expected columns: {missing}"

# Ensure all income values are non-negative
def test_income_positive(cleaned_data):
    assert (cleaned_data["Income"] >= 0).all(), "Income contains negative values."

# Check that the 'Response' column only contains binary values (0 or 1)
def test_response_binary(cleaned_data):
    unique_values = set(cleaned_data["Response"].unique())
    assert unique_values.issubset({0, 1}), f"Unexpected values in 'Response': {unique_values}"
