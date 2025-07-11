from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.fuse_embeddings import fuse_embeddings

router = APIRouter(prefix="/fuse-embeddings", tags=["Fusion"])

@router.post("")
def fuse_embeddings_route():
    try:
        result = fuse_embeddings()
        return {
            "message": "Fusion complete.",
            "time_taken": f"{result['summary']['time_seconds']} seconds",
            "files_processed": result['summary']['processed'],
            "results": result["results"]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
