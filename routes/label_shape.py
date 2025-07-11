from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.label_shape import generate_gpt_labels

router = APIRouter(prefix="/label-shape", tags=["GPT Labeling"])

@router.post("")
def label_shapes():
    try:
        result = generate_gpt_labels()
        return {
            "message": "Labeling complete.",
            "time_taken": f"{result['summary']['time_seconds']} seconds",
            "files_processed": result["summary"]["processed"],
            "results": result["results"]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
