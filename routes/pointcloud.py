
from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from services.pointcloud import process_all_files_to_pointclouds
from pathlib import Path

router = APIRouter(prefix="/pointclouds", tags=["Point Cloud"])

POINTCLOUD_DIR = Path("point_clouds")

# ✅ 1. Generate point clouds for all uploaded files
@router.post("/process")
def convert_all_uploaded_to_pointclouds():
    try:
        result = process_all_files_to_pointclouds()
        return {
            "message": "Point cloud generation completed.",
            "results": result
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ 2. List all point cloud .csv files
@router.get("")
def list_pointclouds():
    if not POINTCLOUD_DIR.exists():
        return JSONResponse(status_code=404, content={"error": "point_clouds directory not found"})

    files = []
    for file in POINTCLOUD_DIR.glob("*.csv"):
        files.append({
            "filename": file.name,
            "size_kb": round(file.stat().st_size / 1024, 2),
            "download_url": f"/pointclouds/download/{file.name}"
        })

    return {
        "message": "Available point cloud CSVs",
        "count": len(files),
        "files": files
    }

# ✅ 3. Download a specific point cloud
@router.get("/download/{filename}")
def download_pointcloud(filename: str):
    file_path = POINTCLOUD_DIR / filename
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"error": f"{filename} not found"})

    return FileResponse(path=file_path, filename=filename, media_type="text/csv")
