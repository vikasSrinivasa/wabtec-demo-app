from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

router = APIRouter(prefix="/labels", tags=["Labels"])
LABEL_DIR = Path("labels")

@router.get("")
def list_label_files():
    if not LABEL_DIR.exists():
        return JSONResponse(status_code=404, content={"error": "labels directory not found"})

    files = []
    for file in LABEL_DIR.glob("*_label.json"):
        files.append({
            "filename": file.name,
            "size_kb": round(file.stat().st_size / 1024, 2),
            "download_url": f"/labels/download/{file.name}"
        })

    return {
        "message": "Available GPT-labeled metadata files",
        "count": len(files),
        "files": files
    }

@router.get("/download/{filename}")
def download_label_file(filename: str):
    file_path = LABEL_DIR / filename
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"error": f"{filename} not found"})

    return FileResponse(path=file_path, filename=filename, media_type="application/json")
