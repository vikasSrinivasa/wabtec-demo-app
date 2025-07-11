# from fastapi import APIRouter
# from fastapi.responses import JSONResponse
# from services.render_views import capture_all_views

# router = APIRouter(prefix="/capture-views", tags=["Rendering"])

# @router.post("")
# def trigger_view_rendering():
#     try:
#         result = capture_all_views()
#         return {
#             "message": "View rendering complete.",
#             "time_taken": f"{result['summary']['time_seconds']} seconds",
#             "files_processed": result['summary']['total_files'],
#             "results": result["results"]
#         }
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.render_views import capture_all_views

router = APIRouter(prefix="/capture-views", tags=["Rendering"])

@router.post("")
def capture_views_endpoint():
    try:
        result = capture_all_views()
        return {
            "message": "Rendered views successfully.",
            "time_taken": f"{result['summary']['time_seconds']} seconds",
            "files_processed": result['summary']['total_files'],
            "results": result["results"]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
