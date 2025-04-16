from sqlalchemy import create_engine

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