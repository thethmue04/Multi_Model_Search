# Multimodal Search Engine with Qdrant and CLIP

A full-stack, distributed Digital Transformation (DX) application that enables real-time multimodal search capabilities. The system processes, vectorizes, and indexes image datasets using OpenAI's CLIP model, allowing users to perform semantic searches through a modern web interface.

---

## 🚀 Key Features
* **Multimodal Embedding Generation:** Leverages the `clip-ViT-B-32` model via SentenceTransformers to map text and images into a shared 512-dimensional vector space.
* **Vector Database Indexing:** Utilizes **Qdrant** with **Cosine Similarity** metrics for high-performance, navigable graph-based nearest neighbor search (HNSW).
* **Automated Data Ingestion:** A robust Python pipeline that extracts local image assets, runs inference to generate embeddings, binds custom payload metadata, and upserts them in batches.
* **Modern Full-Stack Architecture:** Features a fast Python backend alongside a lightweight, reactive Frontend built with Vite and React.
* **Production Ready:** Containerized setup using Docker and integrated with automated GitHub Actions CI/CD workflows.

---

## 📂 Project Architecture

```text
MULTIMODAL_SEARCH/
│
├── .github/workflows/
│   └── deploy.yml          # Automated CI/CD deployment workflow
│
├── backend/
│   ├── Dockerfile          # Container configuration for backend services
│   ├── ingest.py           # Data processing and vector ingestion pipeline
│   ├── main.py             # API server application layer
│   └── requirements.txt    # Python dependencies
│
├── frontend/
│   ├── src/                # React components & main application views
│   ├── Dockerfile          # Container configuration for client hosting
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Frontend build configurations
│
├── my_dataset/             # Local directory for raw image storage (Git ignored)
└── docker-compose.yml      # Orchestration layer for 
```

## Multi-container deployment
```
🛠️ Tech Stack

    Frontend: React, Vite, JavaScript (ES6+)

    Backend Framework: Python, FastAPI / Framework of choice

    AI/ML Infrastructure: SentenceTransformers (clip-ViT-B-32), PIL (Pillow)

    Vector Database: Qdrant (Running via Docker on Port 6333)

    DevOps & CI/CD: Docker, Docker Compose, GitHub Actions
```
---
### 🏁 Getting Started

1. Prerequisites

Ensure you have the following installed on your machine:

    Docker & Docker Compose

    Python 3.10+

    Node.js & npm

2. Environment Setup

Clone the repository and prepare your local media directory:

```Bash
git clone <your-repository-url>
cd MULTIMODAL_SEARCH
mkdir my_dataset
```
Drop the images (.png, .jpg, .jpeg) you wish to index inside the newly created my_dataset/ folder.

3. Launching the Services

Spin up the Qdrant database instance and your environment containers using Docker Compose:
Bash
```
docker-compose up -d
```

4. Running the Ingestion Pipeline

To encode your images into the Qdrant vector collection, navigate to your backend directory, install the dependencies, and run the ingestion script:
Bash
```
cd backend
pip install -r requirements.txt
python ingest.py
```
Upon successful execution, the script automatically verifies or provisions the multimodal_search collection, processes the images, and batch-upserts the 512-dimensional structural points into the cluster.

📊 Database Visualization

Once the ingestion pipeline successfully runs, you can access the Qdrant Web UI Dashboard at http://localhost:6333/dashboard. The visual graph panels illustrate how individual vector points are clustered relative to each other within the HNSW space based on their calculated cosine semantic proximity.

### 💡 Tips for Your Presentation:
* **The "Project Architecture" Section:** Use this part of the README during your presentation slides to show how clean your code separation is (`backend` for AI logic, `frontend` for DX UX).
* **The "Key Features" Section:** Point out the **512 dimensions** and **Cosine Similarity** details—professors and technical reviewers love seeing specific metric definitions right in the documentation!

Author : Thet Hmue Khin