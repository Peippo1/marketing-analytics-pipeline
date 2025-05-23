from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

def get_mysql_engine():
    """
    Create and return a SQLAlchemy engine for MySQL.
    Tries to use Streamlit secrets first (when running in Streamlit Cloud),
    otherwise falls back to environment variables from a .env file.
    """
    try:
        import streamlit as st
        creds = st.secrets["mysql"]
        user = creds["user"]
        password = creds["password"]
        host = creds["host"]
        port = int(creds["port"])
        db = creds["database"]
    except (ImportError, AttributeError, KeyError):
        # Fall back to .env values
        print("🔍 Falling back to local .env for MySQL credentials...")
        load_dotenv()
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        host = os.getenv("MYSQL_HOST")
        port = int(os.getenv("MYSQL_PORT", 3306))
        db = os.getenv("MYSQL_DATABASE")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)

def get_customers_data():
    """
    Retrieve the customers_cleaned table from the MySQL database.
    Returns a pandas DataFrame.
    """
    try:
        engine = get_mysql_engine()
        query = "SELECT * FROM customers_cleaned"
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        print(f"❌ Failed to load customer data: {e}")
        raise