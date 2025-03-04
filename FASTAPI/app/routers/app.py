from fastapi import APIRouter, HTTPException, Query
from services.llm import ollama_use
# from SQLUtility import execute
from backend import Configs
import requests

router = APIRouter()

@router.get("/config/")
def get_config(selected_db: str = None):
    """Returns current database and model configuration. Uses Configs.db_name if no database is selected."""
    database = selected_db if selected_db else Configs.db_name

    return {
        "selected_database": database,
        "model": Configs.llm_model
    }

@router.get("/prompt/")
def process_prompt(
    input_text: str = Query(..., description="Enter your prompt"),
    selected_db: str = None
):
    """Processes the given prompt using LLM and returns the output. Uses Configs.db_name if no database is selected."""
    try:
        database = selected_db if selected_db else Configs.db_name
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
