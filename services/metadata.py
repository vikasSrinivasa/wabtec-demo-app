from pathlib import Path
import json
import time
from services.detailed_step_metdata_extracter2 import extract_metadata as extract_step_metadata
from services.iges_metadata_extracter import extract_iges_metadata
from services.glb_metadata_extracter import extract_glb_metadata

UPLOAD_DIR = Path("uploads")
METADATA_DIR = Path("metadata")
METADATA_DIR.mkdir(exist_ok=True)

def extract_all_metadata():
    start_time = time.time()
    results = []
    supported_exts = [".step", ".stp", ".igs", ".iges", ".glb"]

    for file in UPLOAD_DIR.glob("*"):
        ext = file.suffix.lower()
        if ext not in supported_exts:
            continue

        try:
            if ext in [".step", ".stp"]:
                metadata = extract_step_metadata(str(file))
            elif ext in [".igs", ".iges"]:
                metadata = extract_iges_metadata(str(file))
            elif ext == ".glb":
                metadata = extract_glb_metadata(str(file))
            else:
                raise ValueError("Unsupported format")

            out_path = METADATA_DIR / f"{file.stem}.json"
            with open(out_path, "w") as f:
                json.dump(metadata, f, indent=4)

            results.append({
                "file": file.name,
                "metadata_path": str(out_path),
                "status": "success"
            })

        except Exception as e:
            results.append({
                "file": file.name,
                "error": str(e),
                "status": "failed"
            })

    elapsed = round(time.time() - start_time, 3)
    return {
        "summary": {
            "total_files": len(results),
            "time_seconds": elapsed
        },
        "results": results
    }
