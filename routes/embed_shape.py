from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.embed_shape import embed_all_pointclouds

router = APIRouter(prefix="/embed-shape", tags=["Embedding"])

@router.post("")
def embed_pointclouds():
    try:
        result = embed_all_pointclouds()
        return {
            "message": "Embeddings generated.",
            "results": result
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
