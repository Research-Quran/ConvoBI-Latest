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
import os

DATABASE_FILE = os.path.join(os.path.dirname(__file__), "selected_database.txt")
# Function to read the selected database from the file
def get_selected_database():
    try:
        with open(DATABASE_FILE, "r") as file:
            db_name = file.read().strip()
            if db_name:
                return db_name
    except FileNotFoundError:
        pass
    return Configs.db_name  # Fallback to Configs.db_name if file is missing or empty

# Connect to PostgreSQL
def fetch_pg_cursor():
    db_name = get_selected_database()
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
