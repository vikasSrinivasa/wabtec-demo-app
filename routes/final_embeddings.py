from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

router = APIRouter(prefix="/final-embeddings", tags=["Embeddings (Fused)"])

EMBED_DIR = Path("embeddings_with_metadata")

@router.get("")
def list_final_embeddings():
    if not EMBED_DIR.exists():
        return JSONResponse(status_code=404, content={"error": "No final embeddings found."})

    files = []
    for file in EMBED_DIR.glob("*_final_embed.npy"):
        model = file.stem.replace("_final_embed", "")
        files.append({
            "model": model,
            "filename": file.name,
            "size_kb": round(file.stat().st_size / 1024, 2),
            "download_url": f"/final-embeddings/download/{file.name}"
        })

    return {
        "message": "Available fused embeddings",
        "count": len(files),
        "models": files
    }

@router.get("/download/{filename}")
def download_fused_embedding(filename: str):
    file_path = EMBED_DIR / filename
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"error": f"{filename} not found"})
    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")
