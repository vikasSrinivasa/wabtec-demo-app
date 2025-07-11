from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from services.final_retrieve import final_retrieve

router = APIRouter(prefix="/final-retrieve", tags=["Retrieval (Enriched)"])

@router.post("")
def retrieve_fused_shape(query_model: str = Form(...)):
    try:
        result = final_retrieve(query_model)
        if "error" in result:
            return JSONResponse(status_code=404, content=result)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
