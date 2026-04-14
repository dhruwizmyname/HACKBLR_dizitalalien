import glob
import os
import uuid
from typing import Dict, List

from dotenv import load_dotenv
from langchain_google_vertexai import VertexAIEmbeddings
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

load_dotenv()

# Placeholder: set this in .env with your real GCP project ID.
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").strip()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333").strip()
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "enterprise_kb").strip()

DATA_DIR = os.path.join(os.getcwd(), "data")


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
    chunks: List[str] = []
    if not text.strip():
        return chunks

    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        if txt.strip():
            pages.append(txt)
    return "\n".join(pages)


def ensure_collection(client: QdrantClient, vector_size: int) -> None:
    try:
        client.get_collection(collection_name=QDRANT_COLLECTION)
    except Exception:
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=qmodels.VectorParams(size=vector_size, distance=qmodels.Distance.COSINE),
        )


def main() -> None:
    if not GOOGLE_CLOUD_PROJECT:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is not set. Update .env with your GCP project ID.")

    pdf_paths = sorted(glob.glob(os.path.join(DATA_DIR, "*.pdf")))
    if not pdf_paths:
        print("No PDF files found in ./data. Add PDFs and rerun.")
        return

    print(f"Found {len(pdf_paths)} PDF(s).")
    records: List[Dict[str, str]] = []

    for path in pdf_paths:
        try:
            text = read_pdf(path)
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                records.append({"text": chunk, "source": os.path.basename(path), "chunk_index": i})
            print(f"Ingest prep: {os.path.basename(path)} -> {len(chunks)} chunks")
        except Exception as exc:
            print(f"Skipping {path}: {exc}")

    if not records:
        print("No text chunks extracted from PDFs.")
        return

    embeddings = VertexAIEmbeddings(
        model_name="text-embedding-004",
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_LOCATION,
    )
    qdrant = QdrantClient(url=QDRANT_URL, timeout=30)

    try:
        vectors = embeddings.embed_documents([r["text"] for r in records])
    except Exception as exc:
        raise RuntimeError(f"Failed to generate embeddings from Vertex AI: {exc}") from exc

    if not vectors:
        raise RuntimeError("Embedding API returned no vectors.")

    ensure_collection(qdrant, len(vectors[0]))

    points = []
    for rec, vec in zip(records, vectors):
        points.append(
            qmodels.PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload={
                    "text": rec["text"],
                    "source": rec["source"],
                    "chunk_index": rec["chunk_index"],
                },
            )
        )

    batch_size = 64
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        try:
            qdrant.upsert(collection_name=QDRANT_COLLECTION, points=batch, wait=True)
        except Exception as exc:
            raise RuntimeError(f"Qdrant upsert failed at batch {i // batch_size}: {exc}") from exc

    print(f"Ingestion complete. Upserted {len(points)} chunks into '{QDRANT_COLLECTION}'.")


if __name__ == "__main__":
    main()
