from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import extract_metadata, upload ,embed_shape,retrieve,metadata,render_views,label_shape,labels,fuse_embeddings,final_retrieve,final_embeddings

from routes import pointcloud as pointclouds



app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(upload.router)
app.include_router(pointclouds.router)
app.include_router(embed_shape.router)
app.include_router(retrieve.router)
app.include_router(extract_metadata.router)
app.include_router(metadata.router)  
app.include_router(render_views.router)
app.include_router(labels.router)
app.include_router(label_shape.router)
app.include_router(fuse_embeddings.router)
app.include_router(final_retrieve.router)
app.include_router(final_embeddings.router)
@app.get("/")
def health_check():
    return {"status": "3D API is up!"}
