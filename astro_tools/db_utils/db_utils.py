# db_utils.py
from sqlalchemy import create_engine, text
from contextlib import contextmanager
import os

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME')

# Connection string dla PostgreSQL
engine = create_engine(
    f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
)

@contextmanager
def get_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()

def query(sql, params=None):
    """Szybkie zapytanie - zwraca wyniki"""
    with get_connection() as conn:
        result = conn.execute(text(sql), params or {})
        return result.fetchall()

def query_df(sql, params=None):
    """Zwraca pandas DataFrame"""
    import pandas as pd
    with get_connection() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})
    
def query_scalar(sql, params=None):
    """Zwraca pojedynczą wartość"""
    with get_connection() as conn:
        result = conn.execute(text(sql), params or {})
        return result.scalar()    