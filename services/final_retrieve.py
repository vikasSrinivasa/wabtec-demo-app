import os, time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from collections import defaultdict

EMBED_DIR = "embeddings_with_metadata"

def final_retrieve(query_model: str, top_k: int = 5, n_clusters: int = 5):
    start = time.time()

    vecs = []
    ids = []

    for fname in os.listdir(EMBED_DIR):
        if fname.endswith(".npy"):
            model_id = fname.replace("_final_embed.npy", "")
            ids.append(model_id)
            vecs.append(np.load(os.path.join(EMBED_DIR, fname)))

    vecs = np.vstack(vecs)

    if query_model not in ids:
        return {"error": f"Query model '{query_model}' not found."}

    query_index = ids.index(query_model)
    query_vector = vecs[query_index].reshape(1, -1)

    sim_scores = cosine_similarity(query_vector, vecs).flatten()
    sorted_indices = np.argsort(sim_scores)[::-1]

    top_matches = []
    for i in sorted_indices:
        if i == query_index:
            continue
        top_matches.append({
            "model": ids[i],
            "similarity": round(float(sim_scores[i]), 4)
        })
        if len(top_matches) == top_k:
            break

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(vecs)
    cluster_id = int(labels[query_index])

    cluster_members = [ids[i] for i, label in enumerate(labels) if label == cluster_id]

    clusters = defaultdict(list)
    for i, label in enumerate(labels):
        clusters[int(label)].append(ids[i])

    elapsed = round(time.time() - start, 2)

    return {
        "summary": {
            "query_model": query_model,
            "top_k": top_k,
            "cluster_id": cluster_id,
            "time_seconds": elapsed
        },
        "top_matches": top_matches,
        "cluster_members": cluster_members,
        "all_clusters": dict(clusters)
    }
