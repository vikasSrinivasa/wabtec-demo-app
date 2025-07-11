import torch
import numpy as np
import pandas as pd
from pathlib import Path
from services.pointnet_model import PointNetEncoder  # moved here from your root
import time
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PointNetEncoder().to(device)
model.eval()

POINTCLOUD_DIR = Path("point_clouds")
EMBED_DIR = Path("embeddings")
EMBED_DIR.mkdir(exist_ok=True)

def embed_all_pointclouds():
    start=time.time()
    results = []
    for csv_file in POINTCLOUD_DIR.glob("*.csv"):
        try:
            pts = pd.read_csv(csv_file).values
            if pts.shape[0] > 2048:
                idx = np.random.choice(len(pts), 2048, replace=False)
            else:
                idx = np.random.choice(len(pts), 2048, replace=True)
            sampled = pts[idx]

            tensor = torch.tensor(sampled.T, dtype=torch.float32).unsqueeze(0).to(device)
            with torch.no_grad():
                embedding = model(tensor).cpu().numpy().flatten()

            out_path = EMBED_DIR / f"{csv_file.stem}_embed.npy"
            np.save(out_path, embedding)

            results.append({
                "csv_file": csv_file.name,
                "embedding_path": str(out_path)
            })
        except Exception as e:
            results.append({
                "csv_file": csv_file.name,
                "error": str(e)
            })
    elapsed = round(time.time() - start, 2)
    return {
        "results": results,
        "elapsed_time": elapsed
    }
