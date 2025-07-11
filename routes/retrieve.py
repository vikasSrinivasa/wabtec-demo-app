from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from services.retrieve import run_kmeans_and_similarity

router = APIRouter(prefix="/retrieve-shape", tags=["Retrieval"])

@router.post("")
def shape_retrieval(query_model: str = Form(...)):
    try:
        result = run_kmeans_and_similarity(query_model)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
