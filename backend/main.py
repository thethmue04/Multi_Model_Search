from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from PIL import Image
import io
import os

app = FastAPI(title="Multimodal Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading CLIP model (this takes a moment on first boot)...")
model = SentenceTransformer('clip-ViT-B-32')

# Connect to Qdrant (defaults to the docker service name)
qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant = QdrantClient(host=qdrant_host, port=6333)
COLLECTION_NAME = "multimodal_search"

@app.on_event("startup")
def startup_event():
    if not qdrant.collection_exists(COLLECTION_NAME):
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE)
        )

@app.post("/search")
async def search(query_text: str = Form(None), file: UploadFile = File(None)):
    # 1. Generate Vector Embeddings
    if file:
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes))
        vector = model.encode(img).tolist()
    elif query_text:
        vector = model.encode(query_text).tolist()
    else:
        return {"error": "Provide text or an image to search."}
        
    # 2. Search Vector Database
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=5
    )
    
    # 3. Return results
    return {"results": [{"score": hit.score, "data": hit.payload} for hit in hits]}