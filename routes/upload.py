
# from typing import List
# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import JSONResponse
# from pathlib import Path
# import uuid

# router = APIRouter(prefix="/upload", tags=["Upload"])
# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)

# @router.post("")
# def upload_files(files: List[UploadFile] = File(...)):
#     saved = []

#     for file in files:
#         ext = Path(file.filename).suffix.lower()
#         if ext not in [".step", ".stp", ".igs", ".iges", ".glb"]:
#             continue

#         unique_name = f"{uuid.uuid4().hex}{ext}"
#         save_path = UPLOAD_DIR / unique_name
#         with open(save_path, "wb") as f_out:
#             f_out.write(file.file.read())

#         saved.append({
#             "original_name": file.filename,
#             "saved_name": unique_name,
#             "path": str(save_path)
#         })

#     return {
#         "message": "Upload complete.",
#         "count": len(saved),
#         "files": saved
#     }


from typing import List
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import time 
router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("")
def upload_files(files: List[UploadFile] = File(...)):
    saved = []
    start = time.time()
    for file in files:
        ext = Path(file.filename).suffix.lower()
        if ext not in [".step", ".stp", ".igs", ".iges", ".glb"]:
            continue

        # Optional: remove special characters from name
        clean_name = file.filename.replace(" ", "_").replace("/", "_")
        save_path = UPLOAD_DIR / clean_name

        with open(save_path, "wb") as f_out:
            shutil.copyfileobj(file.file, f_out)

        saved.append({
            "original_name": file.filename,
            "saved_as": clean_name,
            "path": str(save_path)
        })
    elapsed = round(time.time() - start, 2)
    return {
        "message": "Upload complete.",
        "count": len(saved),
        "files": saved,
        "elapsed_time": elapsed
    }
