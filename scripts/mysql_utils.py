from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

def get_mysql_engine():
    """
    Create and return a SQLAlchemy engine for MySQL using Streamlit Cloud secrets.
    """
    creds = st.secrets["mysql"]
    url = f"mysql+pymysql://{creds.user}:{creds.password}@{creds.host}:{creds.port}/{creds.database}"
    return create_engine(url)

def get_customers_data():
    """
    Retrieve the customers_cleaned table from the MySQL database.
    Returns a pandas DataFrame.
    """
    engine = get_mysql_engine()
    query = "SELECT * FROM customers_cleaned"
    df = pd.read_sql(query, con=engine)
    return df