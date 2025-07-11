
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import defaultdict
import time
EMBED_DIR = Path("embeddings")

def run_kmeans_and_similarity(query_model: str, n_clusters=5):
    start = time.time()
    embeddings = []
    ids = []
    for f in EMBED_DIR.glob("*_embed.npy"):
        vec = np.load(f).squeeze()
        embeddings.append(vec)
        ids.append(f.stem.replace("_embed", ""))

    if not embeddings:
        raise ValueError("No embeddings found")

    embeddings = np.stack(embeddings)

    if query_model not in ids:
        raise ValueError(f"Query model '{query_model}' not found")

    query_idx = ids.index(query_model)
    query_vec = embeddings[query_idx].reshape(1, -1)

    # Cosine similarity for all
    sim_scores = cosine_similarity(query_vec, embeddings).flatten()
    cosine_results = [
        {
            "model": ids[i],
            "similarity": round(float(sim_scores[i]), 4)
        } for i in np.argsort(sim_scores)[::-1]
    ]

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    # All clusters
    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[int(label)].append(ids[i])

    elapsed = round(time.time() - start, 2)
    return {
        "query_model": query_model,
        "cosine_similarity_rank": cosine_results,
        "cluster_id": int(labels[query_idx]),
        "cluster_members": clusters[int(labels[query_idx])],
        "all_clusters": dict(clusters), "elapsed_time": elapsed}
