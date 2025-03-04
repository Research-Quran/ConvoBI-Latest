from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse
from services import ConnectNeo4j
from pathlib import Path
from io import BytesIO
from backend import Configs
import shutil
from fastapi.responses import FileResponse
from backend.database import get_db, engine
import os
# from services.files import DB_Workflow

# Initialize Router
router = APIRouter()


@router.post("/process_file/")
async def process_file(
    file: UploadFile = File(...),
    file_option: str = Form("Replace"),
    selected_db_name: str =None,
    db: Session = Depends(get_db)
):
    try:
        selected_db = selected_db_name if selected_db_name else Configs.db_name  # Use db_name if provided, otherwise use default
        excel_file = pd.ExcelFile(file.file)
       

        # Step 1: Create schema
        db.execute(text('CREATE SCHEMA IF NOT EXISTS "genaipoc"'))
        db.commit()

        # Step 2: Check if tables exist and truncate if necessary
        if file_option.upper() == 'REPLACE':
            check_tables_sql = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'genaipoc'
            """
            result = db.execute(text(check_tables_sql))
            existing_tables = [row[0] for row in result]
            
            if existing_tables:
                try:
                    for table in existing_tables:
                        db.execute(text(f'TRUNCATE TABLE "genaipoc"."{table}" CASCADE'))
                    db.commit()
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=500, detail=f"Error truncating tables: {str(e)}")
        
        # Step 3: Create tables if they don't exist
        with open('services/files/DB_Workflow.sql', 'r') as f:
            sql_script = f.read()
        
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement and 'CREATE TABLE' in statement.upper():
                try:
                    db.execute(text(statement))
                    db.commit()
                except Exception as e:
                    if 'already exists' not in str(e):
                        print(f"Warning: Table creation failed: {str(e)}")
                    continue

        # Step 4: Process Excel file and insert into input tables
        for sheet in excel_file.sheet_names:
            table_name = sheet
            print(f"Processing sheet: {sheet}")
            data = pd.read_excel(file.file, sheet_name=sheet)
            try:
                data.to_sql(table_name, engine, schema="genaipoc", if_exists=file_option.lower(), index=False)
                print(f"Data from sheet '{sheet}' successfully inserted into table '{table_name}'")
            except Exception as e:
                print(f"Error inserting data from sheet '{sheet}' into table '{table_name}': {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error inserting data from sheet '{sheet}': {str(e)}")

        # Step 5: Execute workflow SQL for data transformations
        db.execute(text(open('services/files/DB_Workflow.sql', 'r').read()))
        db.commit()

        # Step 6: Populate Neo4j
        ConnectNeo4j.fetch_data_from_neo4j(selected_db)
        print("Graph Database Generated Successfully.")

        return {"message": "File processed successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# Endpoint for downloading metadata template
@router.get("/download_template/")
async def download_template():
    """
    Download metadata template as an Excel file.
    """
    file_path = Path("services/files/Metadata_Template.xlsx")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Template file not found.")

    return FileResponse(
        path=file_path,
        filename="Metadata_Template.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )