from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

router = APIRouter(prefix="/metadata", tags=["Metadata"])

METADATA_DIR = Path("metadata")

@router.get("")
def list_metadata_files():
    if not METADATA_DIR.exists():
        return JSONResponse(status_code=404, content={"error": "metadata directory not found"})

    files = []
    for file in METADATA_DIR.glob("*.json"):
        files.append({
            "filename": file.name,
            "size_kb": round(file.stat().st_size / 1024, 2),
            "download_url": f"/metadata/download/{file.name}"
        })

    return {
        "message": "Available metadata JSON files",
        "count": len(files),
        "files": files
    }

@router.get("/download/{filename}")
def download_metadata_file(filename: str):
    file_path = METADATA_DIR / filename
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"error": f"{filename} not found"})

    return FileResponse(path=file_path, filename=filename, media_type="application/json")
