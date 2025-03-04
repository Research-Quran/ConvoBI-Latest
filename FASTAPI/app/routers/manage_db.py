from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text  # Ensure `text` is imported
from backend.database import get_db

router = APIRouter()

@router.get("/databases/")
def list_all_databases(db: Session = Depends(get_db)):
    """Fetch all available databases in PostgreSQL."""
    try:
        result = db.execute(text("SELECT datname FROM pg_database")).fetchall()
        databases = [row[0] for row in result]  # Extract database names
        return {"databases": databases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/select_database/")
def set_database(db_name: str):
    """Set the selected database."""
    try:
        # Store the selected database in a config file or global state
        return {"message": f"Database '{db_name}' selected successfully..", "selected_db": db_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
