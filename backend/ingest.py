import os
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
# Added Distance and VectorParams imports here
from qdrant_client.models import PointStruct, Distance, VectorParams
from PIL import Image

# Initialize the CLIP model (outputs 512-dimensional vectors)
model = SentenceTransformer('clip-ViT-B-32')
qdrant = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "multimodal_search"
IMAGE_DIR = "./my_dataset" # Create this folder and put some images inside

# --- NEW: Check and Create Collection if it doesn't exist ---
if not qdrant.collection_exists(collection_name=COLLECTION_NAME):
    print(f"Collection '{COLLECTION_NAME}' not found. Creating it...")
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=512,  # clip-ViT-B-32 outputs 512 dimensions
            distance=Distance.COSINE
        ),
    )
# ------------------------------------------------------------

points = []

# Ensure the directory exists so the script doesn't crash
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)
    print(f"Created empty directory '{IMAGE_DIR}'. Please add some images and run again.")
    exit()

print("Encoding dataset...")
for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(IMAGE_DIR, filename)
        img = Image.open(path)
        
        # Generate the vector for the image
        vector = model.encode(img).tolist()
        
        # Prepare the payload for Qdrant
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"filename": filename, "filepath": path}
        ))

# Ensure we actually have data to upload before calling upsert
if points:
    # Insert into database
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Successfully upserted {len(points)} images into Qdrant.")
else:
    print(f"No images found in '{IMAGE_DIR}' to ingest.")