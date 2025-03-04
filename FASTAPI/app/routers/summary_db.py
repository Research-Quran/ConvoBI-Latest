from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import create_engine, text
import pandas as pd
from backend import Configs
import os
# import SQLUtility

router = APIRouter()
DATABASE_FILE = os.path.join(os.path.dirname(__file__), "selected_database.txt")
# DATABASE_FILE = "selected_database.txt"

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

# Function to create database engine
def get_engine(db_name):

    db_url = f"postgresql://{Configs.db_user}:{Configs.db_password}@{Configs.db_host}:{Configs.db_port}/{db_name}"
    return create_engine(db_url)

@router.get("/database_info/")
def get_database_info():
    """Fetch database table details for the given database."""
    db_name = get_selected_database()
    print(f"database selected: {db_name}")
    engine = get_engine(db_name)

    try:
        query = text("""
            SELECT  
                c.table_schema AS schema,
                c.table_name AS table,
                COUNT(c.column_name) AS "No Of Columns",
                pg_size_pretty(pg_total_relation_size(t.oid)) AS size
            FROM 
                information_schema.columns c
            JOIN 
                pg_class t ON c.table_name = t.relname
            JOIN 
                pg_namespace n ON n.oid = t.relnamespace 
                    AND c.table_schema = n.nspname
            WHERE 
                c.table_schema NOT IN ('pg_catalog', 'information_schema')
                AND c.table_schema = 'genaipoc'
            GROUP BY 
                c.table_schema,
                c.table_name,
                t.oid
            ORDER BY 
                c.table_schema,
                c.table_name;
        """)

        with engine.connect() as connection:
            result = connection.execute(query)
            rows = result.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="No data returned from the query")

        # Convert query results into DataFrame
        df = pd.DataFrame(rows, columns=['Schema', 'Table', 'No Of Columns', 'Size'])

        return {
            "selected_database": db_name or Configs.db_name,
            "database_info": df.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")
