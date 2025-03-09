from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text  # Ensure `text` is imported
from backend.database import get_db
from pydantic import BaseModel

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


DATABASE_FILE = "selected_database.txt"  # Make sure this variable is defined

# ✅ Define Pydantic Model for Request Body
class DatabaseRequest(BaseModel):
    db_name: str

@router.post("/select_database/")
def set_database(request: DatabaseRequest):
    """Set the selected database and save it to a file."""
    try:
        # Write the selected database to a file (overwriting existing content)
        with open(DATABASE_FILE, "w") as file:
            file.write(request.db_name)

        return {
            "message": f"Database '{request.db_name}' selected successfully.",
            "selected_db": request.db_name,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))