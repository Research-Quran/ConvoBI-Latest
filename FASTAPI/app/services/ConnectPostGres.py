# from sqlalchemy.orm import Session
# from backend.database import get_db
# from backend.Configs import db_name

# def fetch_pg_cursor(db: Session):
#     """Fetch a connection cursor using SQLAlchemy."""
#     try:
#         # Get the actual connection from the session
#         connection = db.connection()
#         cursor = connection.cursor()
#         return cursor
#     except Exception as e:
#         print(f"Error fetching PostgreSQL cursor: {e}")
#         return None



import sys
from backend import Configs
import psycopg2

# Connect to PostgreSQL
def fetch_pg_cursor(selected_db=None):
    db_name = selected_db or Configs.db_name
    print(db_name)
    
    pg_conn = psycopg2.connect(
        database=db_name,
        user=Configs.db_user,
        password=Configs.db_password,
        host=Configs.db_host,  # or your DB host
        port=Configs.db_port
    )
    
    print(pg_conn)

    pg_cursor = pg_conn.cursor()
    return pg_cursor
