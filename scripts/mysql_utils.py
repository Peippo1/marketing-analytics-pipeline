from sqlalchemy import create_engine
import pandas as pd

def get_mysql_engine(
    user="marketing_user",
    password="marketing_pass",
    host="localhost",
    port=3307,
    db="marketing_db"
):
    """
    Create and return a SQLAlchemy engine for MySQL.

    This connects to a Docker-hosted MySQL container using the provided credentials.
    """
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
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