from fastapi import APIRouter, HTTPException, Query
from services.llm import ollama_use
# from SQLUtility import execute
from backend import Configs
import requests
import os

router = APIRouter()

# DATABASE_FILE = os.path.join(os.path.dirname(__file__), "selected_database.txt")
DATABASE_FILE = "selected_database.txt"
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



@router.get("/config/")
def get_config():
    """Returns model configuration."""

    return {
        "model": Configs.llm_model
    }

@router.get("/prompt/")
def process_prompt(
    input_text: str = Query(..., description="Enter your prompt")
):
    """Processes the given prompt using LLM and returns the output. Uses Configs.db_name if no database is selected."""
    try:
        database = get_selected_database()
        print(f"Using Database: {database}")
        print(f"Prompt entered: {input_text}")

        llm_object = ollama_use()
        llm_output = llm_object.call_llm(input_text)

        return {
            "Database": database,
            "Prompt": input_text,
            "Response": llm_output
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing prompt: {str(e)}")

@router.get("/check_network/")
def check_network_connectivity():
    """Checks network connectivity to a given URL."""
    try:
        URL= Configs.llm_URL
        print(f'Checking URL - {URL}')
        response = requests.get(URL)

        if response.status_code == 200:
            return {"URL": URL, "Status": "Online"}
        else:
            return {"URL": URL, "Status": f"Response code: {response.status_code}"}

    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        raise HTTPException(status_code=500, detail=f"Unable to establish connection: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error occurred: {e}")

@router.get("/import_mapping_data/")
def import_mapping_data():
    """Dummy function to import mapping data (returns False)."""
    return {"import_mapping_data": False}
