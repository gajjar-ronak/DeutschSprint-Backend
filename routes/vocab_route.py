from fastapi import APIRouter
from services.vocab_service import VocabService

vocab_router = APIRouter()

@vocab_router.post("/import-data")
async def import_vocabulary():
    """
    Endpoint to import vocabulary data from a local Excel file into MongoDB.
    """
    # Specify the path to the local Excel file
    file_location = "./data.xlsx"  # Adjust this path based on your folder structure

    # Load the Excel data into the database
    result = VocabService.load_excel_to_db(file_location)

    return result