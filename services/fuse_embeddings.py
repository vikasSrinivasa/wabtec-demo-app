# import os, json, time
# import numpy as np
# from pathlib import Path
# from sentence_transformers import SentenceTransformer

# LABEL_DIR = Path("labels")
# SHAPE_EMBED_DIR = Path("embeddings")
# FUSED_DIR = Path("embeddings_with_metadata")
# FUSED_DIR.mkdir(exist_ok=True)

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def normalize(name: str) -> str:
#     return name.strip().lower().replace(" ", "_").replace("-", "_")

# def fuse_embeddings():
#     start = time.time()
#     results = []

#     label_files = list(LABEL_DIR.glob("*_label.json"))

#     for file in label_files:
#         try:
#             label_data = json.loads(file.read_text())
#             model_name = label_data["model"]
#             norm_name = normalize(model_name)

#             shape_embed_path = SHAPE_EMBED_DIR / f"{norm_name}_point_cloud_embed.npy"
#             if not shape_embed_path.exists():
#                 results.append({"model": model_name, "status": "skipped", "reason": "missing shape embedding"})
#                 continue

#             shape_vec = np.load(shape_embed_path).flatten()

#             # Prepare text for embedding
#             text = f"{label_data['label']}\n\nGeometry:\n{json.dumps(label_data.get('geometry', {}), separators=(',', ':'))}"
#             text_vec = model.encode(text)
#             final_vec = np.concatenate([shape_vec, text_vec])

#             out_path = FUSED_DIR / f"{norm_name}_final_embed.npy"
#             np.save(out_path, final_vec)

#             results.append({"model": model_name, "status": "success", "vector_dim": len(final_vec)})

#         except Exception as e:
#             results.append({"model": file.name, "status": "failed", "error": str(e)})

#     elapsed = round(time.time() - start, 2)
#     return {
#         "summary": {
#             "processed": len(results),
#             "time_seconds": elapsed
#         },
#         "results": results
#     }

import os, json, time
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

LABEL_DIR = Path("labels")
SHAPE_EMBED_DIR = Path("embeddings")
FUSED_DIR = Path("embeddings_with_metadata")
FUSED_DIR.mkdir(exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

def normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "_")

def fuse_embeddings():
    start = time.time()
    results = []

    label_files = list(LABEL_DIR.glob("*_label.json"))

    for file in label_files:
        try:
            label_data = json.loads(file.read_text())
            model_name = label_data["model"]
            norm_name = normalize(model_name)

            # Try all possible file name patterns
            possible_filenames = [
                f"{model_name.strip()}_point_cloud_embed.npy",
                f"{model_name.strip().replace('-', '_')}_point_cloud_embed.npy",
                f"{model_name.strip().replace('_', '-')}_point_cloud_embed.npy",
                f"{norm_name}_point_cloud_embed.npy"
            ]

            shape_embed_path = None
            for fname in possible_filenames:
                fpath = SHAPE_EMBED_DIR / fname
                if fpath.exists():
                    shape_embed_path = fpath
                    break

            if shape_embed_path is None:
                results.append({
                    "model": model_name,
                    "status": "skipped",
                    "reason": f"Missing shape embedding for: {model_name}"
                })
                continue

            shape_vec = np.load(shape_embed_path).flatten()

            text = f"{label_data['label']}\n\nGeometry:\n{json.dumps(label_data.get('geometry', {}), separators=(',', ':'))}"
            text_vec = model.encode(text)
            final_vec = np.concatenate([shape_vec, text_vec])

            out_path = FUSED_DIR / f"{norm_name}_final_embed.npy"
            np.save(out_path, final_vec)

            results.append({
                "model": model_name,
                "status": "success",
                "vector_dim": len(final_vec)
            })

        except Exception as e:
            results.append({
                "model": file.name,
                "status": "failed",
                "error": str(e)
            })

    elapsed = round(time.time() - start, 2)
    return {
        "summary": {
            "processed": len(results),
            "time_seconds": elapsed
        },
        "results": results
    }
