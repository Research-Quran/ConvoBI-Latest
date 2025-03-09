from fastapi import APIRouter
import os
from backend import Configs
router = APIRouter()

# DATABASE_FILE = os.path.join(os.path.dirname(__file__), "selected_database.txt")
DATABASE_FILE = "selected_database.txt"


@router.get("/current_database/")
async def current_database():
    try:
        with open(DATABASE_FILE, "r") as file:
            db_name = file.read().strip()
            if db_name:
                print("file read")
                return {"current_db": db_name}
    except FileNotFoundError:
        pass
    print("config file ..")
    return {"current_db": Configs.db_name} # Fallback to Configs.db_name if file is missing or empty