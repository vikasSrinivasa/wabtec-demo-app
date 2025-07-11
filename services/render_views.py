

import time
from pathlib import Path
from services.step_to_images import render_step_to_images
from services.iges_to_images import render_iges_to_images
from services.glb_to_images import render_views as render_glb_views

UPLOAD_DIR = Path("uploads")
RENDER_DIR = Path("rendered_images")
RENDER_DIR.mkdir(exist_ok=True)

def capture_all_views():
    start = time.time()
    results = []
    supported_exts = [".step", ".stp", ".igs", ".iges", ".glb"]

    for file in UPLOAD_DIR.glob("*"):
        ext = file.suffix.lower()
        try:
            if ext not in supported_exts:
                continue

            if ext in [".step", ".stp"]:
                render_step_to_images(str(file), str(RENDER_DIR))
            elif ext in [".igs", ".iges"]:
                render_iges_to_images(str(file), str(RENDER_DIR))
            elif ext == ".glb":
                render_glb_views(str(file))

            results.append({
                "file": file.name,
                "status": "success"
            })

        except Exception as e:
            results.append({
                "file": file.name,
                "status": "failed",
                "error": str(e)
            })

    elapsed = round(time.time() - start, 3)
    return {
        "summary": {
            "total_files": len(results),
            "time_seconds": elapsed
        },
        "results": results
    }
