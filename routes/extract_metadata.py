from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.metadata import extract_all_metadata
from pathlib import Path
router = APIRouter(prefix="/extract-metadata", tags=["Metadata"])
from fastapi.responses import FileResponse
@router.post("")
def extract_metadata_route():
    try:
        result = extract_all_metadata()
        return {
            "message": "Metadata extraction complete.",
            "time_taken": f"{result['summary']['time_seconds']} seconds",
            "files_processed": result['summary']['total_files'],
            "results": result["results"]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
